from cffi import FFI
ffi = FFI()

pmemobj_structs = """
    /* for pmemobj.py */
    typedef PMEMoid PObjPtr;
    typedef struct {
        PObjPtr type_table;
        PObjPtr root_object;
        PObjPtr clean_shutdown;
        } PRoot;
    typedef struct {
        size_t ob_refcnt;
        size_t ob_type;
        } PObject;
    typedef struct {
        PObject ob_base;
        size_t ob_size;
        } PVarObject;
    typedef struct {
        PVarObject ob_base;
        PObjPtr ob_items;
        size_t allocated;
        } PListObject;
    typedef struct {
        PVarObject ob_base;
        PObjPtr ob_items;
        } PTupleObject;
    typedef struct {
        PObjPtr  key;
        uint64_t hash;
        } PSetEntry;
    typedef struct {
        PObject ob_base;
        size_t fill;
        size_t used;
        size_t mask;
        size_t hash;
        size_t finger;
        PObjPtr table; /* PSetEntry */
        } PSetObject;
    typedef struct {
        PObject ob_base;
        double fval;
        } PFloatObject;
    typedef struct {
        PObject ob_base;
        size_t ma_used;
        PObjPtr ma_keys;            /* PDictKeysObject */
        PObjPtr ma_values;
        } PDictObject;
    typedef struct {
        uint64_t me_hash;
        PObjPtr me_key;
        PObjPtr me_value;           /* Only meaningful for combined table */
        } PDictKeyEntry;
    typedef struct {
        ssize_t dk_refcnt;
        ssize_t dk_size;
      /*dict_lookup_func dk_lookup;*/
        ssize_t dk_usable;
        PDictKeyEntry dk_entries[1];
        } PDictKeysObject;
    typedef struct {
        PObject ob_base;
        PObjPtr ob_dict;
        } PObjectObject;

    """

ffi.set_source("_pmem",
               """
                   #include <libpmem.h>
                   #include <libpmemlog.h>
                   #include <libpmemblk.h>
                   #include <libpmemobj.h>
               """ + pmemobj_structs,
               libraries=['pmem', 'pmemlog', 'pmemblk', 'pmemobj'])

ffi.cdef("""
    /* libpmem */
    typedef int mode_t;

    const char *pmem_errormsg(void);
    void *pmem_map_file(const char *path, size_t len, int flags, mode_t mode,
        size_t *mapped_lenp, int *is_pmemp);
    int pmem_unmap(void *addr, size_t len);
    int pmem_has_hw_drain(void);
    int pmem_is_pmem(void *addr, size_t len);
    const char *pmem_check_version(
        unsigned major_required,
        unsigned minor_required);
    void pmem_persist(void *addr, size_t len);
    int pmem_msync(void *addr, size_t len);
    void pmem_flush(void *addr, size_t len);
    void pmem_drain(void);

    /* libpmemlog */
    #define PMEMLOG_MIN_POOL ...
    typedef struct pmemlog PMEMlogpool;
    typedef int off_t;

    const char *pmemlog_errormsg(void);
    PMEMlogpool *pmemlog_open(const char *path);
    PMEMlogpool *pmemlog_create(const char *path, size_t poolsize, mode_t mode);
    void pmemlog_close(PMEMlogpool *plp);
    size_t pmemlog_nbyte(PMEMlogpool *plp);
    void pmemlog_rewind(PMEMlogpool *plp);
    off_t pmemlog_tell(PMEMlogpool *plp);
    int pmemlog_check(const char *path);
    int pmemlog_append(PMEMlogpool *plp, const void *buf, size_t count);
    const char *pmemlog_check_version(
        unsigned major_required,
        unsigned minor_required);
    void pmemlog_walk(PMEMlogpool *plp, size_t chunksize,
        int (*process_chunk)(const void *buf, size_t len, void *arg),
        void *arg);

    /* libpmemblk */
    #define PMEMBLK_MIN_POOL ...
    #define PMEMBLK_MIN_BLK ...
    typedef struct pmemblk PMEMblkpool;
    const char *pmemblk_errormsg(void);
    PMEMblkpool *pmemblk_open(const char *path, size_t bsize);
    PMEMblkpool *pmemblk_create(const char *path, size_t bsize,
        size_t poolsize, mode_t mode);
    void pmemblk_close(PMEMblkpool *pbp);
    int pmemblk_check(const char *path, size_t bsize);
    size_t pmemblk_bsize(PMEMblkpool *pbp);
    size_t pmemblk_nblock(PMEMblkpool *pbp);
    int pmemblk_read(PMEMblkpool *pbp, void *buf, off_t blockno);
    int pmemblk_write(PMEMblkpool *pbp, const void *buf, off_t blockno);
    int pmemblk_set_zero(PMEMblkpool *pbp, off_t blockno);
    int pmemblk_set_error(PMEMblkpool *pbp, off_t blockno);
    const char *pmemblk_check_version(
        unsigned major_required,
        unsigned minor_required);

    /* libpmemobj */
    typedef ... va_list;
    typedef struct pmemobjpool PMEMobjpool;
    #define PMEMOBJ_MIN_POOL ...
    #define PMEMOBJ_MAX_ALLOC_SIZE ...
    typedef struct pmemoid {
        uint64_t pool_uuid_lo;
        uint64_t off;
    } PMEMoid;
    static const PMEMoid OID_NULL;
    enum pobj_tx_stage {
        TX_STAGE_NONE,
        TX_STAGE_WORK,
        TX_STAGE_ONCOMMIT,
        TX_STAGE_ONABORT,
        TX_STAGE_FINALLY,
        ...
        };

    const char *pmemobj_errormsg(void);
    PMEMobjpool *pmemobj_open(const char *path, const char *layout);
    PMEMobjpool *pmemobj_create(const char *path, const char *layout,
        size_t poolsize, mode_t mode);
    void pmemobj_close(PMEMobjpool *pop);
    int pmemobj_check(const char *path, const char *layout);
    PMEMoid pmemobj_root(PMEMobjpool *pop, size_t size);
    size_t pmemobj_root_size(PMEMobjpool *pop);
    void *pmemobj_direct(PMEMoid oid);
    int pmemobj_tx_begin(PMEMobjpool *pop, void *env, va_list *);
    void pmemobj_tx_abort(int errnum);
    void pmemobj_tx_commit(void);
    int pmemobj_tx_end(void);
    int pmemobj_tx_add_range(PMEMoid oid, uint64_t off, size_t size);
    int pmemobj_tx_add_range_direct(const void *ptr, size_t size);
    PMEMoid pmemobj_tx_alloc(size_t size, uint64_t type_num);
    PMEMoid pmemobj_tx_zalloc(size_t size, uint64_t type_num);
    PMEMoid pmemobj_tx_realloc(PMEMoid oid, size_t size, uint64_t type_num);
    PMEMoid pmemobj_tx_zrealloc(PMEMoid oid, size_t size, uint64_t type_num);
    PMEMoid pmemobj_tx_strdup(const char *s, uint64_t type_num);
    int pmemobj_tx_free(PMEMoid oid);
    enum pobj_tx_stage pmemobj_tx_stage(void);
    PMEMoid pmemobj_first(PMEMobjpool *pop);
    PMEMoid pmemobj_next(PMEMoid oid);
    uint64_t pmemobj_type_num(PMEMoid oid);

""" + pmemobj_structs)

if __name__ == "__main__":
    ffi.compile()
