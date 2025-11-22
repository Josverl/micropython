# Simplification Plan: Remove Async Guards and Sync Fallback Code

## Status: ✅ COMPLETED

## Core Assumptions (as specified by user):

1. **asyncio and pyserial-asyncio are ALWAYS available** when async mode is used
   - No need for ImportError guards around async imports
   - No need to check if async modules are available

2. **Async commands ONLY run over async transports**
   - AsyncSerialTransport is guaranteed when `--async` flag is used
   - All async methods (`*_async()`) are guaranteed to exist on the transport
   - No need for `hasattr()` checks in async command handlers
   - No need for sync fallback branches in async command handlers

## Code to Remove:

### 1. In `commands_async.py`:

#### Remove all `hasattr()` checks for async methods:
- `hasattr(transport, "exec_raw_no_follow_async")`
- `hasattr(transport, "follow_async")`
- `hasattr(transport, "exec_raw_async")`
- `hasattr(transport, "fs_readfile_async")`
- `hasattr(transport, "fs_writefile_async")`
- `hasattr(transport, "fs_hashfile_async")`

#### Remove all sync fallback branches (the `else:` blocks):
In functions like:
- `do_exec_async()` - lines 183-201
- `do_eval_async()` - lines 226-243
- `do_run_async()` - lines 268-283
- `do_filesystem_cp_async()` - various locations
- Any other async functions with sync fallbacks

### 2. In `transport_serial_async.py`:

#### Keep but document the sync wrapper methods:
The sync wrapper methods (lines 183-230):
- `enter_raw_repl()`
- `exit_raw_repl()`
- `exec_raw_no_follow()`
- `follow()`
- `exec_raw()`

**Rationale**: These ARE needed because:
- `State.ensure_raw_repl()` (sync) may be called before async handlers
- nest_asyncio allows these to work within the async event loop
- They provide compatibility layer for code that hasn't been fully converted yet

### 3. No changes needed in `main.py`:
- Import guards are fine (they're for the main entry point)
- The async loop setup is correct

## Expected Benefits:

1. **Reduced Complexity**: Remove ~50-100 lines of dead code
2. **Clearer Intent**: Code clearly shows async-only path
3. **Better Maintainability**: No confusion about which path is taken
4. **Performance**: Slightly faster (no runtime checks)

## Implementation Completed:

### 1. ✅ Simplified `do_exec_async()` (lines 175-201)
- Removed `hasattr(transport, "exec_raw_no_follow_async")` check
- Removed `hasattr(transport, "follow_async")` check  
- Removed all sync fallback branches (`else:` blocks)
- Now directly calls `await transport.exec_raw_no_follow_async()` and `await transport.follow_async()`

### 2. ✅ Simplified `do_eval_async()` (lines 215-243)
- Removed `hasattr(transport, "exec_raw_no_follow_async")` check
- Removed `hasattr(transport, "follow_async")` check
- Removed sync fallback branches
- Now directly calls async methods

### 3. ✅ Simplified `do_run_async()` (lines 260-283)
- Removed `hasattr(transport, "exec_raw_async")` check
- Removed `hasattr(transport, "exec_raw_no_follow_async")` check
- Removed all sync fallback branches
- Now directly calls `await transport.exec_raw_async()` and `await transport.exec_raw_no_follow_async()`

### 4. ✅ Simplified `do_filesystem_cp_async()`
- Removed `hasattr(state.transport, "fs_readfile_async")` check
- Removed `hasattr(state.transport, "fs_writefile_async")` check
- Removed `hasattr(state.transport, "fs_hashfile_async")` check
- Removed all sync fallback branches
- Now directly calls async filesystem methods

### 5. ✅ Removed Fallback Tests
Deleted 7 test functions that tested dead code paths:
- `test_exec_async_fallback_sync()`
- `test_exec_async_fallback_sync_with_follow()`
- `test_exec_async_fallback_sync_with_follow_error()`
- `test_eval_async_fallback_sync()`
- `test_run_async_fallback_sync()`
- `test_filesystem_cp_local_to_remote_fallback_sync()`
- `test_filesystem_cp_remote_to_local_fallback_sync()`

## Results:

### Code Reduction:
- **~80 lines removed** from `commands_async.py` (hasattr checks and else branches)
- **~140 lines removed** from `tests/test_async_commands.py` (fallback tests)
- **Total: ~220 lines of dead code eliminated**

### Test Results:
- ✅ All 28 async command tests pass (was 35, now 28 after removing 7 fallback tests)
- ✅ No functional changes to working code
- ✅ Cleaner, more maintainable codebase

### Code Quality:
- **Clarity**: Async command handlers now clearly show they only work with async transports
- **Simplicity**: No conditional logic for transport method availability
- **Maintainability**: Less code to maintain, no confusion about which path is taken
- **Performance**: Eliminated runtime hasattr() checks
