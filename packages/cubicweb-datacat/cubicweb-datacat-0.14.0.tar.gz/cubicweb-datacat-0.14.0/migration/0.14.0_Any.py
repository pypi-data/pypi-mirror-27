sync_schema_props_perms('dataset_publisher')
add_attribute('ResourceFeed', 'file_name')
for entity in find('ResourceFeed').entities():
    entity.cw_set(file_name=entity.url.split('/')[-1])
commit(ask_confirm=False)

sync_schema_props_perms('license')
