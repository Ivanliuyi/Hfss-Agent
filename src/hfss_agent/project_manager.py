from pathlib import Path
from .aedt_session import AEDTSession


class ProjectManager:
    """负责HFSS工程和Design的创建与管理。"""
    SOLUTION_TYPES = {
        "driven_modal": "DrivenModal",
        "driven_terminal": "DrivenTerminal",
        "eigenmode": "Eigenmode"
    }
    
    def __init__(self, session):
        # 保存外部传入的AEDTSession对象。
        self.session = session

        self.project = None
        self.design = None
        self.solution_type = None
        self.project_path = None
        
    def create_project(self):
        # 创建工程前必须先成功连接AEDT。
        if self.session.desktop is None:
            raise RuntimeError(
                "尚未连接HFSS，请先调用connect()"
            )

        try:
            # NewProject()通过Desktop对象创建一个新工程。
            self.project = self.session.desktop.NewProject()

            return self.project

        except Exception as error:
            raise RuntimeError(
                "创建HFSS工程失败"
            ) from error

    def create_design(
        self,
        design_name,
        solution_type
    ):
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
        hfss_solution_type = self.SOLUTION_TYPES[normalized_type]

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

            # 只有成功取得Design对象后，才能设置求解类型。
            if self.session._needs_classic_network_override():

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
            
    def save_project(self,project_name,output_dir="output"):
        # 保存前必须已经创建Project。
        if self.project is None:
            raise RuntimeError(
                "尚未创建工程，请先调用create_project()"
            )

        # __file__是当前Python文件的位置。
        # parents[2]对应Hfss-Agent项目根目录。
        project_root = Path(__file__).resolve().parents[2]

        output_path = Path(output_dir)

        # 如果传入的是相对路径，则放在项目根目录下面。
        if not output_path.is_absolute():
            output_path = project_root / output_path

        # 文件夹不存在时自动创建。
        output_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # 自动补充HFSS工程扩展名。
        if not project_name.lower().endswith(".aedt"):
            project_name = project_name + ".aedt"

        self.project_path = output_path / project_name

        try:
            # SaveAs第二个参数True表示允许覆盖同名工程。
            self.project.SaveAs(
                str(self.project_path),
                True
            )

            return self.project_path

        except Exception as error:
            raise RuntimeError(
                f"保存HFSS工程失败：{self.project_path}"
            ) from error
            
def main():
    # 第一层：创建并连接AEDT Session。
    session = AEDTSession()
    session.connect()

    # 第二层：把Session对象交给ProjectManager。
    manager = ProjectManager(session)

    project = manager.create_project()

    print("AEDT连接成功")
    print("AEDT版本：", session.aedt_version)
    print("HFSS工程创建成功")
    print("Project对象：", project)
    
    design = manager.create_design(
        design_name="HFSS_Agent_Test",
        solution_type="driven_modal"
    )
    print("HFSS设计创建成功")
    print("Design对象：", design)
    print("求解类型：", manager.solution_type)
    project_path = manager.save_project(
    project_name="HFSS_Agent_Test"
)

    print("HFSS工程保存成功")
    print("Project路径：", project_path)


if __name__ == "__main__":
    main()