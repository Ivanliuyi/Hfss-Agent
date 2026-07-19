import win32com.client
# Com:Component Object Model 
class HFSSController:

    def __init__(
        self,
        prog_id="Ansoft.ElectronicsDesktop"
    ):
        self.prog_id = prog_id
        self.app = None
        self.desktop = None
        self.project = None

    def connect(self):
        try:
            #Dispatch()的作用是根据COM标识找到对应软件，并创建一个Python可以控制的COM代理对象。
            #Ansoft.ElectronicsDesktop是HFSS的COM标识，表示我们要连接的是HFSS软件。
            self.app = win32com.client.Dispatch(
                self.prog_id
            )

            self.desktop = self.app.GetAppDesktop()
            #如果AEDT窗口最小化，就恢复；如果AEDT正在后台运行，就将窗口显示出来；方便当前调试时观察建模过程。
            self.desktop.RestoreWindow()

            return self.desktop

        except Exception as error:
            raise RuntimeError(
                f"无法连接HFSS，ProgID={self.prog_id}"
            ) from error
            
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


def main():
    controller = HFSSController()
    desktop = controller.connect()

    print("HFSS连接成功")
    print("Desktop对象：", desktop)
    
    project = controller.create_project()
    print("HFSS工程创建成功")
    print("Project对象：", project)
    


if __name__ == "__main__":
    main()
    
