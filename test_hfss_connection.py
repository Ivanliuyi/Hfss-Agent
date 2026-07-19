import os
import time
import win32com.client


def main():
    print("[1] 正在连接或启动 Ansys Electronics Desktop...")

    try:
        app = win32com.client.Dispatch("Ansoft.ElectronicsDesktop")
        print("[2] COM对象创建成功")
    except Exception as exc:
        print("[失败] 无法创建Ansoft.ElectronicsDesktop对象")
        print(repr(exc))
        return

    try:
        desktop = app.GetAppDesktop()
        print("[3] 已获取Desktop对象")
    except Exception as exc:
        print("[失败] 无法获取Desktop对象")
        print(repr(exc))
        return

    try:
        desktop.RestoreWindow()
        print("[4] AEDT窗口已显示")
    except Exception as exc:
        print("[提示] RestoreWindow执行失败，但不一定影响后续操作")
        print(repr(exc))

    try:
        project = desktop.NewProject()
        print("[5] 已新建HFSS工程")
    except Exception as exc:
        print("[失败] 无法新建工程")
        print(repr(exc))
        return

    try:
        design = project.InsertDesign(
            "HFSS",
            "HFSS_Agent_Test",
            "DrivenModal",
            ""
        )
        print("[6] 已创建HFSS Driven Modal设计")
    except Exception as exc:
        print("[失败] 无法创建HFSS设计")
        print(repr(exc))
        return

    try:
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)

        project_path = os.path.join(
            output_dir,
            "HFSS_Agent_Connection_Test.aedt"
        )

        project.SaveAs(project_path, True)

        print("[7] 工程保存成功")
        print("工程路径：", project_path)
    except Exception as exc:
        print("[失败] 工程保存失败")
        print(repr(exc))
        return

    time.sleep(2)
    print("[完成] Python调用HFSS的最小测试通过")


if __name__ == "__main__":
    main()