import qbs

MachinekitApplication {
    name: "TCT3D"
    halFiles: ["TCT3D.hal", "TCT3D.postgui.hal"]
    configFiles: ["TCT3D.ini"]
    bbioFiles: ["paralell_cape3.bbio"]
    otherFiles: ["tool.tbl", "pru-stepper.var"]
    pythonFiles: ["python/*"]
    compFiles: ["comp/*"]

    //targetDir: "/home/linuxcnc/unimat5"
    type: "linuxcnc"
}
