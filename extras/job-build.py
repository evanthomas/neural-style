import os

OUTPUT = "jobs.sh"
output_dir = '/home/evan/neurosim/images/outputs'
target_dir = '/home/evan/neurosim/images/content'
style_dir = '/home/evan/neurosim/images/style'
outputs = os.listdir(output_dir)

target_styles = [
    ('_9241468.jpg', 'PC110357.jpg'),
    ('DJI_0176 Panorama_hdr.jpg', 'P1100747.jpg'),
    ('DJI_0689.jpg', 'P6090937.jpg'),
    ('_DSC0708.jpg', 'P9223489.jpg'),
    ('DSC_0911.jpg', 'DSC_3578.jpg'),
    ('DSC_0979.jpg', 'P1130070.jpg'),
    ('_DSC1773.jpg', 'P7010416.jpg'),
    ('DSC_1812.jpg', 'IMG_1291.jpg'),
    ('_DSC3319.jpg', 'PC210096.jpg'),
    ('_DSC3320.jpg', 'IMG_0642.jpg'),
    ('DSC_3520.jpg', '_DSC3684.jpg'),
    ('DSC_4010.jpg', 'P1030440.jpg'),
    ('_DSC4605.jpg', 'DSC_0327.jpg'),
    ('_DSC4612.jpg', 'P1090167.jpg'),
    ('_DSC5735.jpg', '_1020293.jpg'),
    ('DSC_6052.jpg', 'P1140337.jpg'),
    ('_dsc6717.jpg', 'DSC_7650.jpg'),
    ('_DSC6787.jpg', '_7060438.jpg'),
    ('_DSC6815.jpg', '_DSC6076.jpg'),
    ('_DSC7440.jpg', 'PC070012.jpg'),
    ('_DSC7521.jpg', 'KBT_0747.jpg'),
    ('_DSC7696.jpg', 'DSC_7084.jpg'),
    ('DSC_7800.jpg', 'DSCN1281.jpg'),
    ('DSC_7815-Edit.jpg', 'IMG_0755.jpg'),
    ('DSCN0525.jpg', '_DSC2308.jpg'),
    ('KBT_1335.jpg', 'P1140551.jpg'),
    ('KBT_1495.jpg', '_DSC4216.jpg'),
    ('KBT_7626.jpg', 'DSC_8613.jpg'),
    ('P1070282.jpg', 'DSC_6390.jpg'),
    ('P1070621.jpg', '_DSC7491.jpg'),
    ('P9280113.jpg', 'IMG_1585.jpg'),
    ('PA260077.jpg', 'DSC_6098.jpg'),
    ('PB290381.jpg', 'IMG_1585.jpg'),
    ('PC260008.jpg', 'DSC_9311.jpg')
]


scales = [0.05, 0.125, 0.25, 0.5, 1]

f = open(OUTPUT, 'w')
f.write('#!/bin/bash\n\n')
f.write('export CUDA_VISIBLE_DEVICES=0\n\n')

cnt = 0
for (target, style) in target_styles:
    for scale in scales:
        t, _ = os.path.splitext(target)
        s, _ = os.path.splitext(style)

        outputName = t + '__' + s + '__' + str(scale) + '.jpg'
        if outputName in outputs:
            pass
        else:
            cnt = cnt + 1
            full_output_name = os.path.join(output_dir, outputName)
            full_target_name = os.path.join(target_dir, target)
            full_style_name = os.path.join(style_dir, style)
            js = "/home/evan/neurosim/neural-style/extras/specific_launcher.sh \"{target}\" \"{style}\" {scale} \"{full_output_name}\"\n".format(style=full_style_name, target=full_target_name, scale=scale, full_output_name=full_output_name)
            f.write(js)

f.close()

print(str(cnt) + ' jobs created')
