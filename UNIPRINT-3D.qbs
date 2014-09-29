import qbs

MachinekitApplication {
    name: "UNIPRINT-3D"
    halFiles: ["TCT3D-2.hal", "TCT3D.postgui.hal"]
    configFiles: ["TCT3D-2.ini"]
    bbioFiles: ["paralell_cape3.bbio"]
    otherFiles: ["tool.tbl", "pru-stepper.var", "TCT3D.panel.xml", "subroutines"]
    pythonFiles: ["python"]
    compFiles: ["gantry.comp", "led_dim.comp", "thermistor_check.comp"]
    linuxcncIni: "TCT3D-2.ini"
    //display: "thinkpad.local:0.0"
}
