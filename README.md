ake -C /lib/modules/`uname -r`/build M=/home/phanngoctuan/Downloads/os-course/lab/vtfs  modules 
make[1]: Entering directory '/usr/src/linux-headers-6.14.0-35-generic'
make[2]: Entering directory '/home/phanngoctuan/Downloads/os-course/lab/vtfs'
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
  You are using:           gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
  CC [M]  source/vtfs.o
In file included from source/vtfs.c:10:
/usr/src/linux-headers-6.14.0-35-generic/include/linux/lsm_hook_defs.h:29:15: error: expected declaration specifiers or ‘...’ before numeric constant
   29 | LSM_HOOK(int, 0, binder_set_context_mgr, const struct cred *mgr)
      |               ^
/usr/src/linux-headers-6.14.0-35-generic/include/linux/lsm_hook_defs.h:29:18: error: unknown type name ‘binder_set_context_mgr’
   29 | LSM_HOOK(int, 0, binder_set_context_mgr, const struct cred *mgr)
      |                  ^~~~~~~~~~~~~~~~~~~~~~
source/vtfs.c: In function ‘vtfs_init’:
source/vtfs.c:42:20: error: invalid storage class for function ‘vtfs_exit’
   42 | static void __exit vtfs_exit(void) {
      |                    ^~~~~~~~~
In file included from source/vtfs.c:2:
/usr/src/linux-headers-6.14.0-35-generic/include/linux/module.h:131:49: error: invalid storage class for function ‘__inittest’
  131 |         static inline initcall_t __maybe_unused __inittest(void)                \
      |                                                 ^~~~~~~~~~
source/vtfs.c:47:1: note: in expansion of macro ‘module_init’
   47 | module_init(vtfs_init);
      | ^~~~~~~~~~~
source/vtfs.c:47:1: warning: ‘alias’ attribute ignored [-Wattributes]
/usr/src/linux-headers-6.14.0-35-generic/include/linux/module.h:139:49: error: invalid storage class for function ‘__exittest’
  139 |         static inline exitcall_t __maybe_unused __exittest(void)                \
      |                                                 ^~~~~~~~~~
source/vtfs.c:48:1: note: in expansion of macro ‘module_exit’
   48 | module_exit(vtfs_exit);
      | ^~~~~~~~~~~
source/vtfs.c:48:1: warning: ‘alias’ attribute ignored [-Wattributes]
source/vtfs.c:50:22: error: invalid storage class for function ‘vtfs_get_inode’
   50 | static struct inode* vtfs_get_inode(struct super_block *sb, const struct inode *dir, umode_t mode, int i_ino) {
      |                      ^~~~~~~~~~~~~~
source/vtfs.c:60:12: error: invalid storage class for function ‘vtfs_fill_super’
   60 | static int vtfs_fill_super(struct super_block *sb, void *data, int silent) {
      |            ^~~~~~~~~~~~~~~
source/vtfs.c: In function ‘vtfs_fill_super’:
source/vtfs.c:64:22: error: ‘ENOMEN’ undeclared (first use in this function); did you mean ‘ENOMEM’?
   64 |   if(!inode) return -ENOMEN;
      |                      ^~~~~~
      |                      ENOMEM
source/vtfs.c:64:22: note: each undeclared identifier is reported only once for each function it appears in
source/vtfs.c: In function ‘vtfs_init’:
source/vtfs.c:73:23: error: invalid storage class for function ‘vtfs_mount’
   73 | static struct dentry *vtfs_mount(struct file_system_type *fs_type, int flags, const char *token, void *data) {
      |                       ^~~~~~~~~~
source/vtfs.c:86:13: error: invalid storage class for function ‘vtfs_kill_sb’
   86 | static void vtfs_kill_sb(struct super_block *sb) {
      |             ^~~~~~~~~~~~
source/vtfs.c:88:1: error: expected declaration or statement at end of input
   88 | }
      | ^
source/vtfs.c: At top level:
source/vtfs.c:20:23: warning: ‘vtfs_mount’ used but never defined
   20 | static struct dentry* vtfs_mount(struct file_system_type *fs_type, int flags, const char *token, void *data);
      |                       ^~~~~~~~~~
source/vtfs.c:22:13: warning: ‘vtfs_kill_sb’ used but never defined
   22 | static void vtfs_kill_sb(struct super_block *sb);
      |             ^~~~~~~~~~~~
source/vtfs.c:23:12: warning: ‘vtfs_fill_super’ declared ‘static’ but never defined [-Wunused-function]
   23 | static int vtfs_fill_super(struct super_block *sb, void *data, int silent);
      |            ^~~~~~~~~~~~~~~
source/vtfs.c:86:13: warning: ‘vtfs_kill_sb’ defined but not used [-Wunused-function]
   86 | static void vtfs_kill_sb(struct super_block *sb) {
      |             ^~~~~~~~~~~~
source/vtfs.c:73:23: warning: ‘vtfs_mount’ defined but not used [-Wunused-function]
   73 | static struct dentry *vtfs_mount(struct file_system_type *fs_type, int flags, const char *token, void *data) {
      |                       ^~~~~~~~~~
make[4]: *** [/usr/src/linux-headers-6.14.0-35-generic/scripts/Makefile.build:207: source/vtfs.o] Error 1
make[3]: *** [/usr/src/linux-headers-6.14.0-35-generic/Makefile:1997: .] Error 2
make[2]: *** [/usr/src/linux-headers-6.14.0-35-generic/Makefile:251: __sub-make] Error 2
make[2]: Leaving directory '/home/phanngoctuan/Downloads/os-course/lab/vtfs'
make[1]: *** [Makefile:251: __sub-make] Error 2
make[1]: Leaving directory '/usr/src/linux-headers-6.14.0-35-generic'
make: *** [Makefile:8: all] Error 2
