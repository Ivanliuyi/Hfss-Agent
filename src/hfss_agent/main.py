from .aedt_session import AEDTSession
from .project_manager import ProjectManager
from .modeler import Modeler


def main():
    print("[1/8] 创建AEDT会话对象")
    session = AEDTSession()

    print("[2/8] 连接AEDT")
    session.connect()
    print("AEDT连接成功")
    print("Desktop对象：", session.desktop)
    print("AEDT版本：", session.aedt_version)

    print("[3/8] 创建工程管理器")
    manager = ProjectManager(session)

    print("[4/8] 创建HFSS工程")
    manager.create_project()
    print("HFSS工程创建成功")
    print("Project对象：", manager.project)

    print("[5/8] 创建HFSS Design")
    manager.create_design(
        design_name="HFSS_Agent_Test",
        solution_type="driven_modal"
    )
    print("HFSS设计创建成功")
    print("Design对象：", manager.design)
    print("求解类型：", manager.solution_type)

    print("[6/8] 创建并连接3D Modeler")
    modeler = Modeler(manager)
    modeler.connect()
    print("3D Modeler连接成功")
    print("Editor对象：", modeler.editor)

    print("[7/8] 设置模型单位")
    modeler.set_units(
        unit="m",
        rescale=False
    )
    print("模型单位设置成功")
    print("用户标准单位：", modeler.model_unit)
    print("HFSS实际单位：", modeler.hfss_model_unit)

    print("[8/8] 保存HFSS工程")
    manager.save_project(
        project_name="Hfss_Agent_Modeler_Test",
        output_dir=r"E:\PycharmProjects\Hfss-Agent\output"
    )
    print("HFSS工程保存成功")
    print("Project路径：", manager.project_path)

    print("\nHFSS Agent基础流程执行成功")


if __name__ == "__main__":
    main()