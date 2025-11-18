make -C /lib/modules/`uname -r`/build M=/home/phanngoctuan/Downloads/os-course/lab/vtfs  modules 
make[1]: Entering directory '/usr/src/linux-headers-6.14.0-35-generic'
make[2]: Entering directory '/home/phanngoctuan/Downloads/os-course/lab/vtfs'
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
  You are using:           gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
  CC [M]  source/vtfs.o
source/vtfs.c:47:15: warning: no previous prototype for ‘vtfs_get_inode’ [-Wmissing-prototypes]
   47 | struct inode* vtfs_get_inode(struct super_block *sb, const struct inode *dir, umode_t mode, int i_ino) {
      |               ^~~~~~~~~~~~~~
source/vtfs.c: In function ‘vtfs_get_inode’:
source/vtfs.c:51:20: error: passing argument 1 of ‘inode_init_owner’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   51 |   inode_init_owner(&init_user_ns, dir, mode);
      |                    ^~~~~~~~~~~~~
      |                    |
      |                    struct user_namespace *
In file included from /usr/src/linux-headers-6.14.0-35-generic/include/linux/compat.h:17,
                 from /usr/src/linux-headers-6.14.0-35-generic/arch/x86/include/asm/ia32.h:7,
                 from /usr/src/linux-headers-6.14.0-35-generic/arch/x86/include/asm/elf.h:10,
                 from /usr/src/linux-headers-6.14.0-35-generic/include/linux/elf.h:6,
                 from /usr/src/linux-headers-6.14.0-35-generic/include/linux/module.h:19,
                 from source/vtfs.c:2:
/usr/src/linux-headers-6.14.0-35-generic/include/linux/fs.h:2054:41: note: expected ‘struct mnt_idmap *’ but argument is of type ‘struct user_namespace *’
 2054 | void inode_init_owner(struct mnt_idmap *idmap, struct inode *inode,
      |                       ~~~~~~~~~~~~~~~~~~^~~~~
source/vtfs.c:51:35: warning: passing argument 2 of ‘inode_init_owner’ discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
   51 |   inode_init_owner(&init_user_ns, dir, mode);
      |                                   ^~~
/usr/src/linux-headers-6.14.0-35-generic/include/linux/fs.h:2054:62: note: expected ‘struct inode *’ but argument is of type ‘const struct inode *’
 2054 | void inode_init_owner(struct mnt_idmap *idmap, struct inode *inode,
      |                                                ~~~~~~~~~~~~~~^~~~~
source/vtfs.c:51:40: warning: passing argument 3 of ‘inode_init_owner’ makes pointer from integer without a cast [-Wint-conversion]
   51 |   inode_init_owner(&init_user_ns, dir, mode);
      |                                        ^~~~
      |                                        |
      |                                        umode_t {aka short unsigned int}
/usr/src/linux-headers-6.14.0-35-generic/include/linux/fs.h:2055:43: note: expected ‘const struct inode *’ but argument is of type ‘umode_t’ {aka ‘short unsigned int’}
 2055 |                       const struct inode *dir, umode_t mode);
      |                       ~~~~~~~~~~~~~~~~~~~~^~~
source/vtfs.c:51:3: error: too few arguments to function ‘inode_init_owner’
   51 |   inode_init_owner(&init_user_ns, dir, mode);
      |   ^~~~~~~~~~~~~~~~
/usr/src/linux-headers-6.14.0-35-generic/include/linux/fs.h:2054:6: note: declared here
 2054 | void inode_init_owner(struct mnt_idmap *idmap, struct inode *inode,
      |      ^~~~~~~~~~~~~~~~
source/vtfs.c: At top level:
source/vtfs.c:57:8: error: expected ‘{’ before ‘int’
   57 | struct int vtfs_fill_super(struct super_block *sb, void *data, int silent) {
      |        ^~~
source/vtfs.c:57:8: error: two or more data types in declaration specifiers
source/vtfs.c: In function ‘vtfs_mount’:
source/vtfs.c:73:45: error: ‘vtfs_fill_super’ undeclared (first use in this function); did you mean ‘vtfs_kill_sb’?
   73 |   entry = mount_nodev(fs_type, flags, data, vtfs_fill_super);
      |                                             ^~~~~~~~~~~~~~~
      |                                             vtfs_kill_sb
source/vtfs.c:73:45: note: each undeclared identifier is reported only once for each function it appears in
cc1: some warnings being treated as errors
make[4]: *** [/usr/src/linux-headers-6.14.0-35-generic/scripts/Makefile.build:207: source/vtfs.o] Error 1
make[3]: *** [/usr/src/linux-headers-6.14.0-35-generic/Makefile:1997: .] Error 2
make[2]: *** [/usr/src/linux-headers-6.14.0-35-generic/Makefile:251: __sub-make] Error 2
make[2]: Leaving directory '/home/phanngoctuan/Downloads/os-course/lab/vtfs'
make[1]: *** [Makefile:251: __sub-make] Error 2
make[1]: Leaving directory '/usr/src/linux-headers-6.14.0-35-generic'
make: *** [Makefile:8: all] Error 2
