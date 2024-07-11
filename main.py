file =  open("./diff.txt","r")
lines = file.readlines()
bases = {
    "Dev":{},
    "Live": {}
}

for line in lines:
    print(line[0])
    if line[0] == "<":
        
        print("Dev")
        
        dev_sql_line = line[1:].split()
        print(dev_sql_line)
        
        table_name = dev_sql_line[0]
        column_name = dev_sql_line[1]
        column_type = dev_sql_line[2]
        column_not_null = dev_sql_line[3]
        
        if len(dev_sql_line)>=5:
            column_default_value = dev_sql_line[4]
        
        if table_name not in bases["Dev"]:
            bases["Dev"][table_name] = {}
            
        bases["Dev"][table_name][column_name] = {
            "column_type": column_type,
            "column_not_null": column_not_null,
            "column_default_value": column_default_value if len(line)>=5 else ""
        }
        
            
        
    elif line[0] == ">":
        
        print("Live")
        
        live_sql_line = line[1:].split()
        print(live_sql_line)
        
        table_name = live_sql_line[0]
        column_name = live_sql_line[1]
        column_type = live_sql_line[2]
        column_not_null = live_sql_line[3]
        
        if len(live_sql_line)>=5:
            column_default_value = live_sql_line[4]
        
        if table_name not in bases["Live"]:
            bases["Live"][table_name] = {}
            
        bases["Live"][table_name][column_name] = {
            "column_type": column_type,
            "column_not_null": column_not_null,
            "column_default_value": column_default_value if len(line)>=5 else ""
        }



tables_live = bases["Live"]
tables_dev = bases["Dev"]

drop_tables = []

# se existe em dev e não existe em live, dropa
for table in tables_dev:
    if table not in tables_live:
        drop_tables.append(f"DROP TABLE `{table}`")
        
print(drop_tables)

drop_column = []

#se a coluna exite em dev mas não existe em live, dropa
for table in tables_dev:
    
    if table in tables_live:
        for column in tables_dev[table]:
            if column not in tables_live[table]:
                drop_column.append(f"ALTER TABLE `{table}` DROP COLUMN `{column}`")
                
print(drop_column)

create_column = []

# se a coluna não existe em dev, mas existe em live e é not null cria
for table in tables_live:
    
    if table in tables_dev:
        for column in tables_live[table]:
            if column not in tables_dev[table]:
                create_column.append(f"ALTER TABLE `{table}` ADD `{column}` {tables_live[table][column]["column_type"]}")
                
print(create_column)