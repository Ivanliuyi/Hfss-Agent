import os
import win32com.client


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
PROJECT_PATH = os.path.join(
    OUTPUT_DIR,
    "HFSS_Agent_Parameterized_Model.aedt"
)


def add_variable(design, name, value):
    """添加HFSS局部设计变量。"""
    design.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                ["NAME:PropServers", "LocalVariables"],
                [
                    "NAME:NewProps",
                    [
                        "NAME:" + name,
                        "PropType:=",
                        "VariableProp",
                        "UserDef:=",
                        True,
                        "Value:=",
                        value,
                    ],
                ],
            ],
        ]
    )


def create_box(editor, name, x, y, z, dx, dy, dz, material, color):
    """创建三维实体。"""
    editor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:=", x,
            "YPosition:=", y,
            "ZPosition:=", z,
            "XSize:=", dx,
            "YSize:=", dy,
            "ZSize:=", dz,
        ],
        [
            "NAME:Attributes",
            "Name:=", name,
            "Flags:=", "",
            "Color:=", color,
            "Transparency:=", 0.5,
            "PartCoordinateSystem:=", "Global",
            "UDMId:=", "",
            "MaterialValue:=", '"' + material + '"',
            "SurfaceMaterialValue:=", '""',
            "SolveInside:=", True,
        ],
    )


def create_rectangle(editor, name, x, y, z, width, height, material):
    """在XY平面创建矩形金属片。"""
    editor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:=", True,
            "XStart:=", x,
            "YStart:=", y,
            "ZStart:=", z,
            "Width:=", width,
            "Height:=", height,
            "WhichAxis:=", "Z",
        ],
        [
            "NAME:Attributes",
            "Name:=", name,
            "Flags:=", "",
            "Color:=", "(255 128 0)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:=", "",
            "MaterialValue:=", '"' + material + '"',
            "SurfaceMaterialValue:=", '""',
            "SolveInside:=", False,
        ],
    )


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("[0] Script entered")

    app = win32com.client.Dispatch("Ansoft.ElectronicsDesktop")
    desktop = app.GetAppDesktop()
    desktop.RestoreWindow()

    print("[1] AEDT started")

    project = desktop.NewProject()
    design = project.InsertDesign(
        "HFSS",
        "HFSS_Agent_Model",
        "DrivenModal",
        "",
    )

    editor = design.SetActiveEditor("3D Modeler")
    editor.SetModelUnits(
        [
            "NAME:Units Parameter",
            "Units:=", "mm",
            "Rescale:=", False,
        ]
    )

    print("[2] Design created and units set")

    variables = {
        "sub_l": "40mm",
        "sub_w": "40mm",
        "sub_h": "1.6mm",
        "patch_l": "12mm",
        "patch_w": "16mm",
        "feed_l": "14mm",
        "feed_w": "3mm",
        "metal_t": "0.035mm",
    }

    for variable_name, variable_value in variables.items():
        add_variable(design, variable_name, variable_value)

    print("[3] Design variables created")

    # 基板：中心位于坐标原点附近
    create_box(
        editor=editor,
        name="Substrate",
        x="-sub_w/2",
        y="-sub_l/2",
        z="0mm",
        dx="sub_w",
        dy="sub_l",
        dz="sub_h",
        material="FR4_epoxy",
        color="(143 175 143)",
    )

    # 接地板：位于基板底部
    create_rectangle(
        editor=editor,
        name="Ground",
        x="-sub_w/2",
        y="-sub_l/2",
        z="0mm",
        width="sub_w",
        height="sub_l",
        material="copper",
    )

    # 矩形贴片：位于基板顶部
    create_rectangle(
        editor=editor,
        name="Patch",
        x="-patch_w/2",
        y="-patch_l/2",
        z="sub_h",
        width="patch_w",
        height="patch_l",
        material="copper",
    )

    # 馈线：从基板下边缘连接至贴片
    create_rectangle(
        editor=editor,
        name="FeedLine",
        x="-feed_w/2",
        y="-sub_l/2",
        z="sub_h",
        width="feed_w",
        height="sub_l/2-patch_l/2",
        material="copper",
    )

    print("[4] Substrate, ground, patch and feed line created")

    project.SaveAs(PROJECT_PATH, True)

    print("[5] Project saved")
    print("工程路径：", PROJECT_PATH)
    print("[完成] 参数化几何建模测试通过")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("[失败] 参数化建模过程中出现错误")
        print(type(error).__name__ + ":", error)
        raise