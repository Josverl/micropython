import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestMPRemoteFileSystem:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Create temporary directory for test files
        self.tmp_dir = tempfile.mkdtemp()
        
        # Create ramdisk script
        with open(f"{self.tmp_dir}/ramdisk.py", "w") as f:
            f.write("""
class RAMBlockDev:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)

    def readblocks(self, block_num, buf):
        for i in range(len(buf)):
            buf[i] = self.data[block_num * self.block_size + i]

    def writeblocks(self, block_num, buf):
        for i in range(len(buf)):
            self.data[block_num * self.block_size + i] = buf[i]

    def ioctl(self, op, arg):
        if op == 4: # get number of blocks
            return len(self.data) // self.block_size
        if op == 5: # get block size
            return self.block_size

import os

bdev = RAMBlockDev(512, 50)
os.VfsFat.mkfs(bdev)
os.mount(bdev, '/ramdisk')
os.chdir('/ramdisk')
""")
        
        yield
        
        # Clean up temporary directory
        shutil.rmtree(self.tmp_dir)
    
    def run_mpremote(self, cmd):
        """Run mpremote command and return stdout"""
        full_cmd = f"mpremote {cmd}"
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        # if result.returncode != 0 and "expect error" not in cmd:
        #     pytest.fail(f"Command failed: {full_cmd}\nError: {result.stderr}")
        return result.stdout
    
    def setup_ramdisk(self):
        """Mount ramdisk on device"""
        self.run_mpremote(f"run {self.tmp_dir}/ramdisk.py")

    def sha256(self, data):
        """Calculate local SHA256 checksum"""
        return hashlib.sha256(data).digest().hex()

    def file_sha256(self, filename:str):
        with open(f"{self.tmp_dir}/{filename}", "rb") as f:
            data = f.read()
        local_hash = self.sha256(data)
        return local_hash
    
    def create_test_package(self,name:str="package"):
        os.makedirs(f"{self.tmp_dir}/{name}/subpackage", exist_ok=True)
        
        with open(f"{self.tmp_dir}/{name}/__init__.py", "w") as f:
            f.write("from .x import x\nfrom .subpackage import y\n")
        
        with open(f"{self.tmp_dir}/{name}/x.py", "w") as f:
            f.write('def x():\n  print("x")\n')
        
        with open(f"{self.tmp_dir}/{name}/subpackage/__init__.py", "w") as f:
            f.write("from .y import y\n")
        
        with open(f"{self.tmp_dir}/{name}/subpackage/y.py", "w") as f:
            f.write('def y():\n  print("y")\n')    

    def test_basic_operations(self):
        """Test basic file operations"""
        self.setup_ramdisk()
        output = self.run_mpremote("resume ls")
        # assert output.strip() == ""
        
        # Create and verify empty files
        self.run_mpremote("resume touch a.py")
        self.run_mpremote("resume touch :b.py")
        output = self.run_mpremote("resume ls :")
        assert "0 a.py\n" in output, f"Expected '0 a.py' in output, got {output}"
        assert "0 b.py\n" in output, f"Expected '0 b.py' in output, got {output}"
        
        # Verify file contents and checksums
        output = self.run_mpremote("resume sha256sum a.py")
        remote_hash = output.split()[-1]
        source_hash = self.sha256(b'')
        assert remote_hash == source_hash , f"Checksum mismatch: {remote_hash} != {source_hash}"

    
    def test_file_copy_operations(self):
        """Test file copy operations"""
        # Create test file
        with open(f"{self.tmp_dir}/a.py", "w") as f:
            f.write('print("Hello")\nprint("World")\n')
        
        self.setup_ramdisk()
        
        # Copy file to device in various ways
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :b.py")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :c.py")
        self.run_mpremote("resume cp :a.py :d.py")
        
        # Verify files exist
        output = self.run_mpremote("resume ls")
        assert "a.py" in output
        assert "b.py" in output
        assert "c.py" in output
        assert "d.py" in output
        
        # Verify files can be imported
        output = self.run_mpremote('resume exec "import a; import b; import c"')
        assert output.count("Hello") == 3, f"Expected 'Hello' to occur 3 times, got {output.count('Hello')}"
        assert output.count("World") == 3, f"Expected 'World' to occur 3 times, got {output.count('World')}"

        # Verify file checksums
        output = self.run_mpremote("resume sha256sum a.py")
        local_hash = self.file_sha256("a.py")
        assert local_hash.split()[0] in output


    
    def test_directory_operations(self):
        """Test directory and subdirectory operations"""
        with open(f"{self.tmp_dir}/a.py", "w") as f:
            f.write('print("Hello")\nprint("World")\n')
            
        self.setup_ramdisk()
        
        # Create directories and copy files into them
        self.run_mpremote("resume mkdir aaa")
        self.run_mpremote("resume mkdir :bbb")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :aaa")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :bbb/b.py")
        
        # Verify files in subdirectories
        output = self.run_mpremote("resume cat :aaa/a.py bbb/b.py")
        assert "Hello" in output
        assert "World" in output
    
    def test_force_copy(self):
        """Test cp -f (force copy)."""
        with open(f"{self.tmp_dir}/a.py", "w") as f:
            f.write('print("Hello")\nprint("World")\n')
            
        self.setup_ramdisk()
        self.run_mpremote("resume mkdir aaa")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :aaa")
        self.run_mpremote(f"resume cp -f {self.tmp_dir}/a.py :aaa")
        
        output = self.run_mpremote("resume cat :aaa/a.py")
        assert "Hello" in output
        assert "World" in output
    
    def test_copy_with_trailing_slash(self):
        """Test cp where the destination has a trailing /."""
        with open(f"{self.tmp_dir}/a.py", "w") as f:
            f.write('print("Hello")\nprint("World")\n')
            
        self.setup_ramdisk()
        self.run_mpremote("resume mkdir aaa")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :aaa/")
        
        # This should fail (copying to a file path with trailing slash)
        output = self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :aaa/a.py/ || echo 'expect error'")
        assert "expect error" in output
    
    def test_remove_operations(self):
        """Test removing files and directories"""
        with open(f"{self.tmp_dir}/a.py", "w") as f:
            f.write('print("Hello")\nprint("World")\n')
            
        self.setup_ramdisk()
        
        # Create files and directories
        self.run_mpremote("resume mkdir aaa bbb")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :b.py")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :c.py")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :aaa/a.py")
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :bbb/b.py")
        
        # Remove files
        self.run_mpremote("resume rm :b.py c.py")
        output = self.run_mpremote("resume ls")
        assert "b.py" not in output
        assert "c.py" not in output
        
        # Remove files from subdirectories and then the directories
        self.run_mpremote("resume rm :aaa/a.py bbb/b.py")
        self.run_mpremote("resume rmdir aaa :bbb")
        output = self.run_mpremote("resume ls")
        assert "aaa" not in output
        assert "bbb" not in output
    
    def test_edit_file(self, monkeypatch):
        """Test the edit command"""
        with open(f"{self.tmp_dir}/a.py", "w") as f:
            f.write('print("Hello")\nprint("World")\n')
            
        self.setup_ramdisk()
        self.run_mpremote(f"resume cp {self.tmp_dir}/a.py :d.py")
        
        # Edit the file to replace "Hello" with "Goodbye"
        if os.name == "nt":
            # On Windows, use Powerhell script to edit the file
            monkeypatch.setenv("EDITOR", f"pwsh {Path(__file__).parent / 'pwsh_sed.ps1'}",)
        else:
            # On Unix-like systems, use sed
             monkeypatch.setenv("EDITOR","sed -i s/Hello/Goodbye/")
        self.run_mpremote("resume edit d.py")
        
        # Verify the file was modified
        output = self.run_mpremote('resume exec "import d"')
        assert "Goodbye" in output
    
    def test_recursive_copy_local_to_device(self):
        """Create a local directory structure and copy it to `:` on the device."""
        self.setup_ramdisk()
        
        # Copy package to device root
        self.create_test_package()
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :")
        
        # Verify directory structure
        output = self.run_mpremote("resume ls : :package :package/subpackage")
        assert "package" in output
        assert "__init__.py" in output
        assert "x.py" in output
        assert "y.py" in output
        
        # Verify imports work
        output = self.run_mpremote('resume exec "import package; package.x(); package.y()"')
        assert "x" in output
        assert "y" in output
    
    def test_recursive_copy_with_dest_name(self):
        """Same thing except with a destination directory name."""
      
        self.setup_ramdisk()
        
        # Copy package to device with different name
        self.create_test_package()
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :package2")
        
        # Verify directory structure
        output = self.run_mpremote("resume ls : :package2 :package2/subpackage")
        assert "package2" in output
        assert "__init__.py" in output
        assert "x.py" in output
        assert "y.py" in output
        
        # Verify imports work
        output = self.run_mpremote('resume exec "import package2; package2.x(); package2.y()"')
        assert "x" in output
        assert "y" in output
    
    def test_recursive_copy_to_existing_dir(self):
        """Copy to an existing directory, it will be copied inside."""
        
        self.create_test_package()
        self.setup_ramdisk()
        
        # Create directory and copy package into it
        self.run_mpremote("resume mkdir :test")
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :test")
        
        # Verify directory structure
        output = self.run_mpremote("resume ls :test :test/package :test/package/subpackage")
        assert "package" in output
        assert "__init__.py" in output
        assert "x.py" in output
    
    def test_recursive_copy_to_non_existing_subdir(self):
        """Copy to non-existing sub-directory."""
        # Create package structure (reusing from previous test setup)
        self.create_test_package()
        
        self.setup_ramdisk()
        self.run_mpremote("resume mkdir :test")
        
        # Copy to a non-existing subdirectory
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :test/package2")
        
        # Verify directory structure
        output = self.run_mpremote("resume ls :test :test/package2 :test/package2/subpackage")
        assert "package2" in output
        assert "__init__.py" in output
        assert "x.py" in output
    
    def test_recursive_copy_device_to_local(self):
        """Copy from the device back to local."""
        # Create package structure and copy to device
        self.create_test_package()
        
        self.setup_ramdisk()
        self.run_mpremote("resume mkdir :test")
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :test")
        
        # Create local directory and copy from device
        os.makedirs(f"{self.tmp_dir}/copy", exist_ok=True)
        self.run_mpremote(f"resume cp -r :test/package {self.tmp_dir}/copy")
        
        # Verify local directory structure
        assert os.path.exists(f"{self.tmp_dir}/copy/package")
        assert os.path.exists(f"{self.tmp_dir}/copy/package/__init__.py")
        assert os.path.exists(f"{self.tmp_dir}/copy/package/subpackage")
    
    def test_recursive_copy_device_to_local_with_dest_name(self):
        """Copy from the device back to local with destination directory name."""
        # Setup from previous test
        self.create_test_package()
        
        self.setup_ramdisk()
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :")
        
        # Create local directory and copy from device with specific name
        os.makedirs(f"{self.tmp_dir}/copy", exist_ok=True)
        self.run_mpremote(f"resume cp -r :package {self.tmp_dir}/copy/package2")
        
        # Verify local directory structure
        assert os.path.exists(f"{self.tmp_dir}/copy/package2")
        assert os.path.exists(f"{self.tmp_dir}/copy/package2/__init__.py")
        assert os.path.exists(f"{self.tmp_dir}/copy/package2/subpackage")
    
    def test_recursive_copy_device_to_device(self):
        """Copy from device to another location on the device with destination directory name."""
        # Setup
        self.create_test_package()
        
        self.setup_ramdisk()
        
        # Copy to device then to another location on device
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :")
        self.run_mpremote("resume cp -r :package :package3")
        
        # Verify directory structure
        output = self.run_mpremote("resume ls : :package3 :package3/subpackage")
        assert "package3" in output
        assert "__init__.py" in output
        assert "x.py" in output
    
    def test_recursive_copy_device_to_existing_dir(self):
        """Copy from device to another location on the device into an existing directory."""
        # Setup
        self.create_test_package()
        
        self.setup_ramdisk()
        
        # Copy to device, create directory, then copy to that directory
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :")
        self.run_mpremote("resume mkdir :package4")
        self.run_mpremote("resume cp -r :package :package4")
        
        # Verify directory structure
        output = self.run_mpremote("resume ls : :package4 :package4/package :package4/package/subpackage")
        assert "package4" in output
        assert "package" in output
        assert "__init__.py" in output
    
    def test_modified_file_copy(self):
        """Repeat an existing copy with one file modified."""
        # Setup package with initial content
        self.create_test_package()
        
        self.setup_ramdisk()
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :")
        
        # Modify a file and copy again
        with open(f"{self.tmp_dir}/package/subpackage/y.py", "w") as f:
            f.write('def y():\n  print("y2")\n')
            
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :")
        
        # Verify the file was updated
        output = self.run_mpremote('resume exec "import package; package.x(); package.y()"')
        assert "y2" in output


    
    def test_recursive_remove(self):
        """Test rm -r functionality"""
        # Setup
        self.create_test_package()
        
        self.setup_ramdisk()
        self.run_mpremote("resume mkdir :testdir")
        self.run_mpremote(f"resume cp -r {self.tmp_dir}/package :testdir/package")
        
        # Verify directory exists
        output = self.run_mpremote("resume ls :testdir")
        assert "package" in output
        
        # Remove directory recursively
        self.run_mpremote("resume rm -r :testdir/package")
        
        # Verify directory is gone
        output = self.run_mpremote("resume ls :testdir")
        assert "package" not in output
    
    def test_recursive_remove_nonexistent(self):
        """Test rm -r on non-existent path"""
        self.setup_ramdisk()
        output = self.run_mpremote("resume rm -r :nonexistent || echo 'expect error'")
        assert "expect error" in output
    