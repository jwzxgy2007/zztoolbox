
import os,sys,re
def cleanExt(ext):
    while ext.startswith("."):
        ext = ext[1:]
    return ext
def main():
    values = [("folder", lux.DIALOG_FOLDER, "Folder to import from:", None),
              ("output", lux.DIALOG_FOLDER, "Folder to outut:", None),
              ("iext", lux.DIALOG_TEXT, "Input file format to read:", "obj"),
              ("oext", lux.DIALOG_TEXT, "Output image format:", "png"),
              ("width", lux.DIALOG_INTEGER, "Output width:", 1920),
              ("height", lux.DIALOG_INTEGER, "Output height:", 1080),
              ("time", lux.DIALOG_INTEGER, "render time second:", 90),
              ("num", lux.DIALOG_INTEGER, "number of image:", 200)
              ]

    opts = lux.getInputDialog(title = "Render",
                              desc = "Render model",
                              values = values)



    if not opts: 
        return

    if len(opts["folder"]) == 0:
        raise Exception("Folder cannot be empty!")
    fld = opts["folder"]
    if len(opts["iext"]) == 0:
        raise Exception("Input extension cannot be empty!")
    iext = cleanExt(opts["iext"])
    reFiles = re.compile(".*{}".format(iext))
    found = False
    for f in os.listdir(fld):
        if reFiles.match(f):
            found = True
            break
    if not found:
        raise Exception("Could not find any input files matching the extension \"{}\" in \"{}\"!"
                        .format(iext, fld))

    if len(opts["oext"]) == 0:
        raise Exception("Output extension cannot be empty!")
    oext = cleanExt(opts["oext"])

    width = opts["width"]
    height = opts["height"]
    time = opts["time"]
    num = opts["num"]
    output_path = opts['output']

    idx = 0
    env = lux.getActiveEnvironment()
    lux.setSphericalCamera(90,0,0)
    lux.setCameraDistance(3)
    lux.setCameraLookAt(pt=(0,0.45,0))
    env.setBackgroundColor((255,255,255))
    opts = lux.getRenderOptions()
    opts.setMaxTimeRendering(time)

    for f in [f for f in os.listdir(fld) if f.endswith(iext)]:
        path = fld + os.path.sep + f
        opp = lux.getImportOptions()
        opp['retain_materials']=True
        opp['separate_materials']=True
        lux.importFile(path, showOpts = False,opts = opp)

        root = lux.getSceneTree()
        # print(f[:-4])
        obj=root.find(name = f[:-4])[0]
        # idx = idx + 1

        lux.renderImage(output_path+"/"+f[:-4]+'_'+str(0)+'.png', width = 1920, height = 1080, opts = opts)
        for i in range(1,num+1):
            mat = luxmath.Matrix().makeIdentity()
            mat = mat.rotateAroundAxis(luxmath.Vector((0, 1, 0)), 360/num)
            obj.applyTransform(mat)
            lux.renderImage(output_path+"/"+f[:-4]+'_'+str(i)+'.png', width = 1920, height = 1080, opts = opts)
        obj.hide()
main()
