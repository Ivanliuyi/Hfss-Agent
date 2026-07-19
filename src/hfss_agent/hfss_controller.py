import win32com.client
# Com:Component Object Model 
class HFSSController:
    
    # 左边是Agent使用的标准名称，右边是HFSS COM要求的名称。
    SOLUTION_TYPES = {
        "driven_modal": "DrivenModal",
        "driven_terminal": "DrivenTerminal",
        "eigenmode": "Eigenmode"
    }
    
    def __init__(
        self,
        prog_id="Ansoft.ElectronicsDesktop"
    ):
        self.aedt_version = None
        self.prog_id = prog_id
        self.app = None
        self.desktop = None
        self.project = None
        self.design = None
        self.solution_type = None

    def connect(self):
        try:
            #Dispatch()的作用是根据COM标识找到对应软件，并创建一个Python可以控制的COM代理对象。
            #Ansoft.ElectronicsDesktop是HFSS的COM标识，表示我们要连接的是HFSS软件。
            self.app = win32com.client.Dispatch(
                self.prog_id
            )
            self.desktop = self.app.GetAppDesktop()
            # 保存AEDT版本，用于处理不同版本的接口差异。
            self.aedt_version = str(self.desktop.GetVersion())
            #如果AEDT窗口最小化，就恢复；如果AEDT正在后台运行，就将窗口显示出来；方便当前调试时观察建模过程。
            self.desktop.RestoreWindow()

            return self.desktop

        except Exception as error:
            raise RuntimeError(
                f"无法连接HFSS，ProgID={self.prog_id}"
            ) from error
    
    def _needs_classic_network_override(self):
        # 没有获得版本信息时，不执行新版专用操作。
        if self.aedt_version is None:
            return False

        try:
            # "2024.1.0"按"."拆分后，第一个数字是主版本2024。
            version_parts = self.aedt_version.split(".")
            major_version = int(version_parts[0])

            return major_version >= 2024

        except (ValueError, IndexError):
            # 无法识别版本格式时，优先保持旧版兼容行为。
            return False
            
    def create_project(self):
        # 创建工程前必须先成功连接AEDT。
        if self.desktop is None:
            raise RuntimeError(
                "尚未连接HFSS，请先调用connect()"
            )

        try:
            # NewProject()通过Desktop对象创建一个新工程。
            self.project = self.desktop.NewProject()

            return self.project

        except Exception as error:
            raise RuntimeError(
                "创建HFSS工程失败"
            ) from error

    def create_design(self,design_name,solution_type):
        # Design必须创建在Project中。
        if self.project is None:
            raise RuntimeError(
                "尚未创建工程，请先调用create_project()"
            )

        # 去除首尾空格并转换为小写，统一用户输入格式。
        normalized_type = solution_type.strip().lower()
        
        # 防止Agent向HFSS传入不支持的求解类型。
        if normalized_type not in self.SOLUTION_TYPES:
            supported = ", ".join(
                self.SOLUTION_TYPES.keys()
            )
            raise ValueError(
                f"不支持的求解类型：{solution_type}；"
                f"可选类型：{supported}"
            )

        # 将Agent使用的名称转换为HFSS要求的COM名称。
        hfss_solution_type = self.SOLUTION_TYPES[solution_type]

        try:
            self.project.InsertDesign(
                "HFSS",
                design_name,
                hfss_solution_type,
                ""
            )

            # SetActiveDesign()负责激活设计，但不同版本下返回值可能不一致。
            self.project.SetActiveDesign(design_name)

            # 主动获取当前激活的Design对象。
            self.design = self.project.GetActiveDesign()

            if self.design is None:
                raise RuntimeError(
                    f"无法获取HFSS设计对象：{design_name}"
                )
            self.design = self.project.GetActiveDesign()

            # 只有成功取得Design对象后，才能设置求解类型。
            if self._needs_classic_network_override():

                if normalized_type == "driven_modal":
                    self.design.SetSolutionType(
                        "HFSS Modal Network",
                        [
                            "NAME:Options",
                            "EnableAutoOpen:=",
                            False
                        ]
                    )

                elif normalized_type == "driven_terminal":
                    self.design.SetSolutionType(
                        "HFSS Terminal Network",
                        [
                            "NAME:Options",
                            "EnableAutoOpen:=",
                            False
                        ]
                    )
            self.solution_type = normalized_type
            return self.design

        except Exception as error:
            raise RuntimeError(
                f"创建HFSS设计失败：{design_name}"
            ) from error


def main():
    controller = HFSSController()
    desktop = controller.connect()

    print("HFSS连接成功")
    print("Desktop对象：", desktop)
    
    project = controller.create_project()
    print("HFSS工程创建成功")
    print("Project对象：", project)
    
    design = controller.create_design(
        design_name="HFSS_Agent_Test",
        solution_type="driven_modal"
    )
    print("HFSS设计创建成功")
    print("Design对象：", design)
    print("求解类型：", controller.solution_type)
    print("AEDT版本：", controller.aedt_version)


if __name__ == "__main__":
    main()
    
