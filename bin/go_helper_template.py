res_field_content = ""  # ex:Item *Table
res_field_init_content = ""  # ex:helper.Item = NewTable()
res_load = ""  # ex: err = helper.Item.LoadItemConf()
res_load_funcs = ""  # ex:LoadItemConf

code_template_replace_str = "$XXXX"
go_load_funcs_template = """
func ($XXXX *Table) Load$XXXXConf() error {

	// 表加载前清除之前的手动索引和表关联数据
	$XXXX.RegisterPreEntry(func(tab *Table) error {
		return nil
	})

	// 表加载和构建索引后，需要手动处理数据的回调
	$item.RegisterPostEntry(func(tab *Table) error {
		return nil
	})

	return tabtoy.LoadFromFile($XXXX, "./$XXXX.json") // todo 这里记得更改
}
"""

go_load_err_template = """
	err = helper.$XXXX.Load$XXXXConf()
	if err != nil {panic(err)}
"""

go_helper_template = f"""package conf

type Helper struct {{
	$res_field_content
}}

func NewHelper() *Helper {{
	helper := &Helper{{}}

	$res_field_init_content
	return helper
}}

func LoadAllTable(helper *Helper) {{
	if helper == nil {{
		return
	}}
	
	var err error
	
	$res_load
}}

$res_load_funcs
"""
