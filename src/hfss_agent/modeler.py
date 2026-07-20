from .project_manager import ProjectManager


class Modeler:
    """负责HFSS模型单位、设计变量和几何建模操作。"""

    # 左侧是Agent或用户使用的标准单位名称，
    # 右侧是HFSS COM接口实际要求的单位名称。
    UNIT_TYPES = {
        "nm": "nm",
        "um": "um",
        "mm": "mm",
        "cm": "cm",
        "m": "meter",
        "meter": "meter",
        "mil": "mil",
        "in": "in",
        "ft": "ft"
    }

    def __init__(self, project_manager: ProjectManager):
        """
        初始化Modeler。

        Parameters
        ----------
        project_manager : ProjectManager
            已经创建Project和Design的工程管理器对象。
        """

        if not isinstance(project_manager, ProjectManager):
            raise TypeError(
                "project_manager必须是ProjectManager对象"
            )

        # 保存外部传入的ProjectManager。
        self.project_manager = project_manager

        # HFSS的3D Modeler编辑器COM对象。
        self.editor = None

        # 记录用户输入的标准单位，例如m、mm、um。
        self.model_unit = None

        # 记录HFSS实际接收的单位，例如meter、mm、um。
        self.hfss_model_unit = None

    def connect(self):
        """
        获取当前HFSS Design中的3D Modeler编辑器对象。

        Returns
        -------
        object
            HFSS 3D Modeler的COM对象。
        """

        # 必须先创建HFSS Design。
        if self.project_manager.design is None:
            raise RuntimeError(
                "尚未创建HFSS Design，无法获取3D Modeler；"
                "请先调用ProjectManager.create_design()"
            )

        try:
            # 激活当前Design中的3D Modeler编辑器。
            self.editor = (
                self.project_manager.design.SetActiveEditor(
                    "3D Modeler"
                )
            )

            if self.editor is None:
                raise RuntimeError(
                    "HFSS没有返回3D Modeler对象"
                )

            return self.editor

        except Exception as error:
            raise RuntimeError(
                "连接HFSS 3D Modeler失败"
            ) from error

    def set_units(
        self,
        unit: str = "mm",
        rescale: bool = False
    ):
        """
        设置HFSS模型单位。

        Parameters
        ----------
        unit : str
            模型单位，例如nm、um、mm、cm、m、mil、in、ft。

        rescale : bool
            是否按照新单位重新缩放现有模型。

            False：
                只修改单位名称，不重新缩放已有几何尺寸。

            True：
                修改单位时，同时重新缩放已有几何尺寸。

        Returns
        -------
        str
            HFSS实际使用的单位名称。
        """

        # 必须先连接3D Modeler。
        if self.editor is None:
            raise RuntimeError(
                "尚未连接3D Modeler，请先调用Modeler.connect()"
            )

        if not isinstance(unit, str):
            raise TypeError(
                "unit必须是字符串"
            )

        if not isinstance(rescale, bool):
            raise TypeError(
                "rescale必须是布尔值True或False"
            )

        # 去除首尾空格，并转为小写，统一输入格式。
        normalized_unit = unit.strip().lower()

        if normalized_unit not in self.UNIT_TYPES:
            supported = ", ".join(
                sorted(self.UNIT_TYPES.keys())
            )

            raise ValueError(
                f"不支持的模型单位：{unit}；"
                f"可选单位：{supported}"
            )

        # 将Agent使用的标准单位转换为HFSS要求的名称。
        hfss_unit = self.UNIT_TYPES[normalized_unit]

        try:
            self.editor.SetModelUnits(
                [
                    "NAME:Units Parameter",
                    "Units:=",
                    hfss_unit,
                    "Rescale:=",
                    rescale
                ]
            )

            # 保存单位状态，供Agent后续查询。
            self.model_unit = normalized_unit
            self.hfss_model_unit = hfss_unit

            return hfss_unit

        except Exception as error:
            raise RuntimeError(
                f"设置HFSS模型单位失败："
                f"{unit} -> {hfss_unit}"
            ) from error


def main():
    """
    单独运行modeler.py时执行的测试程序。

    推荐的正式运行方式仍然是通过项目主入口main.py调用。
    """

    from .aedt_session import AEDTSession
    from .project_manager import ProjectManager

    # 1. 创建并连接AEDT会话。
    session = AEDTSession()
    session.connect()

    # 2. 创建ProjectManager。
    manager = ProjectManager(session)

    # 3. 创建HFSS工程。
    manager.create_project()

    # 4. 创建HFSS Design。
    manager.create_design(
        design_name="HFSS_Agent_Modeler_Test",
        solution_type="driven_modal"
    )

    # 5. 创建Modeler。
    modeler = Modeler(manager)

    # 6. 连接3D Modeler。
    editor = modeler.connect()

    # 7. 设置模型单位。
    hfss_unit = modeler.set_units(
        unit="m",
        rescale=False
    )

    print("Modeler测试成功")
    print("3D Modeler对象：", editor)
    print("用户输入单位：", modeler.model_unit)
    print("HFSS实际单位：", hfss_unit)


if __name__ == "__main__":
    main()