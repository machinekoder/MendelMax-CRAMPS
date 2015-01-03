import qbs

MachinekitApplication {
    name: "UNIPRINT-3D"
    halFiles: ["UNIPRINT-3D.hal"]
    configFiles: ["UNIPRINT-3D.ini"]
    bbioFiles: ["paralell_cape3.bbio"]
    otherFiles: ["tool.tbl", "subroutines"]
    pythonFiles: ["python"]
    compFiles: ["led_dim.comp", "thermistor_check.comp", "gantry.comp"]
    linuxcncIni: "UNIPRINT-3D.ini"
    //display: "thinkpad.local:0.0"
}
