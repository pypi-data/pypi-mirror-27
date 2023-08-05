"""SECCOMP policy.

This policy is based on the default Docker SECCOMP policy profile. It
allows several syscalls, which are most commonly used. We make one major
change regarding the network-related ``socket`` syscall in that we only
allow AF_INET/AF_INET6 SOCK_DGRAM/SOCK_STREAM sockets for TCP and UDP
protocols.
"""
# pylint: disable=too-many-lines
SECCOMP_POLICY = {
    "defaultAction": "SCMP_ACT_ERRNO",
    "architectures": [
        "SCMP_ARCH_X86_64",
        "SCMP_ARCH_X86",
        "SCMP_ARCH_X32"
    ],
    "syscalls": [
        {
            "name": "accept",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "accept4",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "access",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "alarm",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "bind",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "brk",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "capget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "capset",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "chdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "chmod",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "chown",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "chown32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "clock_getres",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "clock_gettime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "clock_nanosleep",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "close",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "connect",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "copy_file_range",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "creat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "dup",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "dup2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "dup3",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_create1",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_ctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_ctl_old",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_pwait",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_wait",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_wait_old",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "eventfd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "eventfd2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "execve",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "execveat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "exit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "exit_group",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "faccessat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fadvise64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fadvise64_64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fallocate",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fanotify_mark",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchmod",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchmodat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchown",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchown32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchownat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fcntl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fcntl64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fdatasync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fgetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "flistxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "flock",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fork",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fremovexattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fsetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstatat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstatfs",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstatfs64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fsync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ftruncate",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ftruncate64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "futex",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "futimesat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getcpu",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getcwd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getdents",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getdents64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getegid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getegid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "geteuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "geteuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgroups",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgroups32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getitimer",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpeername",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpgrp",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getppid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpriority",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getrandom",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getrlimit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "get_robust_list",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getrusage",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getsid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getsockname",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getsockopt",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "get_thread_area",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "gettid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "gettimeofday",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_add_watch",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_init",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_init1",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_rm_watch",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_cancel",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ioctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_destroy",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_getevents",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ioprio_get",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ioprio_set",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_setup",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_submit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ipc",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "kill",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lchown",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lchown32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lgetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "link",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "linkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "listen",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "listxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "llistxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "_llseek",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lremovexattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lseek",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lsetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lstat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lstat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "madvise",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "memfd_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mincore",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mkdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mkdirat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mknod",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mknodat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mlock",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mlock2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mlockall",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mmap",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mmap2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mprotect",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_getsetattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_notify",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_open",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_timedreceive",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_timedsend",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_unlink",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mremap",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgrcv",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgsnd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "munlock",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "munlockall",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "munmap",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "nanosleep",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "newfstatat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "_newselect",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "open",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "openat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pause",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "personality",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 0,
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                }
            ]
        },
        {
            "name": "personality",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 8,
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                }
            ]
        },
        {
            "name": "personality",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 4294967295,
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                }
            ]
        },
        {
            "name": "pipe",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pipe2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "poll",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ppoll",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "prctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pread64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "preadv",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "prlimit64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pselect6",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pwrite64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pwritev",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "read",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readahead",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readlink",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readlinkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readv",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "recv",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "recvfrom",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "recvmmsg",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "recvmsg",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "remap_file_pages",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "removexattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rename",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "renameat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "renameat2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "restart_syscall",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rmdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigaction",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigpending",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigprocmask",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigqueueinfo",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigreturn",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigsuspend",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigtimedwait",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_tgsigqueueinfo",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getaffinity",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getparam",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_get_priority_max",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_get_priority_min",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getscheduler",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_rr_get_interval",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setaffinity",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setparam",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setscheduler",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_yield",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "seccomp",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "select",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semop",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semtimedop",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "send",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sendfile",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sendfile64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sendmmsg",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sendmsg",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sendto",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgroups",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgroups32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setitimer",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setpgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setpriority",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setregid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setregid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setreuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setreuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setrlimit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "set_robust_list",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setsid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setsockopt",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "set_thread_area",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "set_tid_address",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmdt",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shutdown",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sigaltstack",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "signalfd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "signalfd4",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sigreturn",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "socketpair",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "splice",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "stat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "stat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "statfs",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "statfs64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "symlink",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "symlinkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sync_file_range",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "syncfs",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sysinfo",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "syslog",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "tee",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "tgkill",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "time",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_delete",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timerfd_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timerfd_gettime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timerfd_settime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_getoverrun",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_gettime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_settime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "times",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "tkill",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "truncate",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "truncate64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ugetrlimit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "umask",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "uname",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "unlink",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "unlinkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "utime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "utimensat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "utimes",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "vfork",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "vmsplice",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "wait4",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "waitid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "waitpid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "write",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "writev",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "arch_prctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "modify_ldt",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "chroot",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "clone",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 2080505856,
                    "valueTwo": 0,
                    "op": "SCMP_CMP_MASKED_EQ"
                }
            ]
        },
        {
            "name": "socket",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 12,  # AF_INET
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 1,
                    "value": 1,  # SOCK_STREAM
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 2,
                    "value": 6,  # IPPROTO_TCP
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
            ]
        },
        {
            "name": "socket",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 2,  # AF_INET
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 1,
                    "value": 2,  # SOCK_DGRAM
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 2,
                    "value": 17,  # IPPROTO_UDP
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
            ]
        },
        {
            "name": "socket",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 10,  # AF_INET6
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 1,
                    "value": 1,  # SOCK_STREAM
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 2,
                    "value": 6,  # IPPROTO_TCP
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
            ]
        },
        {
            "name": "socket",
            "action": "SCMP_ACT_ALLOW",
            "args": [
                {
                    "index": 0,
                    "value": 10,  # AF_INET6
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 1,
                    "value": 2,  # SOCK_DGRAM
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
                {
                    "index": 2,
                    "value": 17,  # IPPROTO_UDP
                    "valueTwo": 0,
                    "op": "SCMP_CMP_EQ"
                },
            ]
        },
    ]
}
