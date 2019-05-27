
var SelectInit = function (defaultProjectId, defaultModuleId) {
    var cmbProject = document.getElementById("selectProject");
    var cmbModule = document.getElementById("selectModule");

    var dataList = [];

    //设置默认选中的选项
    function setDefaultOption(obj, id) {
        for (var i = 0; i < obj.options.length; i++) {
            if (obj.options[i].value == id) {
                obj.selectedIndex = i;
                return;
            }
        }
    }

    //创建下拉选项
    function addOption(cmb, obj) {
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = obj.name;
        option.value = obj.id;
    }

    //改变项目
    function changeProject() {
        cmbModule.options.length = 0;
        var pid = cmbProject.options[cmbProject.selectedIndex].value;

        for (let i = 0; i < dataList.length; i++) {
            if(dataList[i].id == pid) {
                let modules = dataList[i].moduleList;
                for(let j=0; j< modules.length; j++){
                    addOption(cmbModule, modules[j]);
                }
            }

        }
        setDefaultOption(cmbModule, defaultModuleId);
    }

    function getSelectData() {
        // 调用获取select数据列表
        $.get("/testcase/get_select_data", {}, function (resp) {
            if (resp.status === 10200) {
                dataList = resp.data;
                //遍历项目
                for (var i = 0; i < dataList.length; i++) {
                    addOption(cmbProject, dataList[i]);
                }

                setDefaultOption(cmbProject, defaultProjectId);
                changeProject();
                cmbProject.onchange = changeProject;
            }
            setDefaultOption(cmbProject, defaultProjectId);
        });
    }

    // 调用getSelectData函数
    getSelectData();

};

var TestCaseInit = function () {

    var url = document.location;
    var cid =  url.pathname.split("/")[3];

    $.post("/testcase/get_case_info",
    {
        cid: cid,
    },
    function (resp, status) {
        console.log("返回的结果", resp.data);

        //url
        document.querySelector("#request_url").value = resp.data.url;

        // 请求方法
        if (resp.data.method == 1){
            document.querySelector("#get").setAttribute("checked", "");
        }
        else if (resp.data.method == 2) {
            document.querySelector("#post").setAttribute("checked", "");
        }
        //请求头
        document.querySelector("#request_header").value = resp.data.header;

        //请求参数类型
        if (resp.data.parameter_type == 1) {
            document.querySelector("#form").setAttribute("checked", "");
        }
        else if (resp.data.parameter_type == 2) {
            document.querySelector("#json").setAttribute("checked", "");
        }

        //请求参数的值
        document.querySelector("#request_parameter").value = resp.data.parameter_body;

        //断言的类型
        if (resp.data.assert_type == 1) {
            document.querySelector("#contains").setAttribute("checked", "");
        }
        else if (resp.data.assert_type == 2) {
            document.querySelector("#mathches").setAttribute("checked", "");
        }

        //断言的值
        document.querySelector("#assert").value = resp.data.assert_text;

        //用例的名称
        document.querySelector("#case_name").value = resp.data.name;

        SelectInit(resp.data.project_id, resp.data.module_id);

    });

}