import qbs

MachinekitApplication {
    name: "TCT3D"
    halFiles: ["TCT3D.hal", "TCT3D.postgui.hal"]
    configFiles: ["TCT3D.ini"]
    bbioFiles: ["paralell_cape3.bbio"]
    otherFiles: ["tool.tbl", "pru-stepper.var", "TCT3D.panel.xml", "subroutines"]
    pythonFiles: ["python"]
    compFiles: ["gantry.comp", "led_dim.comp"]
    linuxcncIni: "TCT3D.ini"
    display: "thinkpad.local:0.0"
}
