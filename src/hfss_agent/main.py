from aedt_session import AEDTSession
from project_manager import ProjectManager

def main():
    # 第一层：建立AEDT连接和版本状态。
    session = AEDTSession()
    desktop = session.connect()

    print("AEDT连接成功")
    print("Desktop对象：", desktop)
    print("AEDT版本：", session.aedt_version)

    # 第二层：管理Project、Design和工程文件。
    manager = ProjectManager(session)

    project = manager.create_project()

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