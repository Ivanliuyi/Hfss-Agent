import win32com.client

class AEDTSession:
    """负责AEDT连接、版本信息及版本兼容判断。"""
        # 左边是Agent使用的标准名称，右边是HFSS COM要求的名称。
    
    def __init__(self, prog_id="Ansoft.ElectronicsDesktop"):
        self.prog_id = prog_id
        self.app =  None
        self.desktop = None
        self.aedt_version = None
        
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
        
def main():
    # 本文件被直接运行时，只测试AEDT连接模块。
    session = AEDTSession()
    desktop = session.connect()

    print("AEDT连接成功")
    print("Desktop对象：", desktop)
    print("AEDT版本：", session.aedt_version)
    print(
        "是否需要修正Hybrid：",
        session._needs_classic_network_override()
    )


if __name__ == "__main__":
    main()