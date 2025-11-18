#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/printk.h>
#include <linux/pagemap.h>
#include <linux/mount.h>
#include <linux/namei.h>
#include <linux/time.h>

#define MODULE_NAME "vtfs"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("secs-dev");
MODULE_DESCRIPTION("A simple FS kernel module");

#define LOG(fmt, ...) pr_info("[" MODULE_NAME "]: " fmt, ##__VA_ARGS__)

// Forward declarations
static struct dentry* vtfs_mount(struct file_system_type *fs_type,
                                 int flags,
                                 const char *token,
                                 void *data);

static void vtfs_kill_sb(struct super_block *sb);
static int vtfs_fill_super(struct super_block *sb, void *data, int silent);

// Filesystem type structure
static struct file_system_type vtfs_fs_type = {
    .owner  = THIS_MODULE,
    .name   = "vtfs",
    .mount  = vtfs_mount,
    .kill_sb = vtfs_kill_sb,
};


// --------------------------- INIT / EXIT ----------------------------------

static int __init vtfs_init(void)
{
    LOG("VTFS module loaded\n");

    int ret = register_filesystem(&vtfs_fs_type);
    if (ret != 0)
        LOG("Failed to register filesystem\n");

    return ret;
}

static void __exit vtfs_exit(void)
{
    unregister_filesystem(&vtfs_fs_type);
    LOG("VTFS module unloaded\n");
}

module_init(vtfs_init);
module_exit(vtfs_exit);


// --------------------------- INODE CREATION --------------------------------

static struct inode* vtfs_get_inode(struct super_block *sb,
                                    const struct inode *dir,
                                    umode_t mode,
                                    int i_ino)
{
    struct inode *inode = new_inode(sb);
    if (!inode)
        return NULL;

    // Correct kernel 6.14 API
    inode_init_owner(&nop_mnt_idmap, inode, dir, mode);
    inode->i_ino = i_ino;

    return inode;
}


// -------------------------- SUPERBLOCK INIT --------------------------------

static int vtfs_fill_super(struct super_block *sb, void *data, int silent)
{
    struct inode *inode;

    inode = vtfs_get_inode(sb, NULL, S_IFDIR | 0755, 1000);
    if (!inode)
        return -ENOMEM;

    sb->s_root = d_make_root(inode);
    if (!sb->s_root)
        return -ENOMEM;

    printk(KERN_INFO "VTFS: superblock created\n");
    return 0;
}


// -------------------------- MOUNT & UNMOUNT --------------------------------

static struct dentry *vtfs_mount(struct file_system_type *fs_type,
                                 int flags,
                                 const char *token,
                                 void *data)
{
    struct dentry *entry;

    entry = mount_nodev(fs_type, flags, data, vtfs_fill_super);

    if (!entry)
        printk(KERN_ERR "VTFS: mount failed\n");
    else
        printk(KERN_INFO "VTFS: mounted successfully\n");

    return entry;
}

static void vtfs_kill_sb(struct super_block *sb)
{
    printk(KERN_INFO "VTFS: superblock destroyed, unmounted\n");
}
