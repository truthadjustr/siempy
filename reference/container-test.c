#include <net-snmp/net-snmp-config.h>
#include <net-snmp/library/container.h>
#include <net-snmp/library/tools.h>

#include <stdio.h>
#include <malloc.h>

struct my_hash_entry {
   char *key;
   char *value;
};

void do_something(void *data, void *context) {
    struct my_hash_entry *entry = data;
    
    printf("%10s: %s\n", entry->key, entry->value);
}

int my_key_compare(struct my_hash_entry *left, struct my_hash_entry *right) {
    return strcmp(left->key, right->key);
}

struct my_hash_entry *
create_hash_entry(char *key, char *value) {
    struct my_hash_entry *entry = SNMP_MALLOC_STRUCT(my_hash_entry);
    entry->key = strdup(key);
    entry->value = strdup(value);
    return entry;
}

int
main() {

    netsnmp_container *container;

    init_snmp("container-test");

    container = netsnmp_container_find("binary_array");
    container->compare = (netsnmp_container_compare*) my_key_compare;

    CONTAINER_INSERT(container, create_hash_entry("pizza",   "yummy"));
    CONTAINER_INSERT(container, create_hash_entry("veggies", "ehhhh"));
    CONTAINER_INSERT(container, create_hash_entry("donuts",  "mmmmmmmmmm"));

    CONTAINER_FOR_EACH(container, do_something, NULL);
}
