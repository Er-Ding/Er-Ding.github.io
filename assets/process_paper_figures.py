import os
from PIL import Image

src_dir = "/Volumes/disk2/CV/assets/paper_extracted"
dst_dir = "/Volumes/disk2/CV/assets"

# 1. TIM Paper - Real Trajectory Comparison (pptx_image48.png)
im_traj = Image.open(os.path.join(src_dir, "pptx_image48.png"))
im_traj.save(os.path.join(dst_dir, "paper-tim-trajectory.png"), "PNG")
print("Saved paper-tim-trajectory.png:", im_traj.size)

# 2. TIM Paper - Error Analysis & Coordinate Transformation (pptx_image29 & pptx_image30 combined)
im_surf1 = Image.open(os.path.join(src_dir, "pptx_image29.png"))
im_surf2 = Image.open(os.path.join(src_dir, "pptx_image30.png"))
# Create side-by-side composite for the research figure banner
w1, h1 = im_surf1.size
w2, h2 = im_surf2.size
comp_w = w1 + w2
comp_h = max(h1, h2)
comp_surf = Image.new("RGB", (comp_w, comp_h), (255, 255, 255))
comp_surf.paste(im_surf1, (0, 0))
comp_surf.paste(im_surf2, (w1, 0))
comp_surf.save(os.path.join(dst_dir, "paper-tim-error-manifold.png"), "PNG")
print("Saved paper-tim-error-manifold.png:", comp_surf.size)

# 3. TIM Paper - Radar & RTK Experimental Platform (pptx_image46.jpeg)
im_platform = Image.open(os.path.join(src_dir, "pptx_image46.jpeg"))
im_platform.save(os.path.join(dst_dir, "paper-tim-platform.jpg"), "JPEG", quality=95)
print("Saved paper-tim-platform.jpg:", im_platform.size)

# 4. ICCC Paper - Real CDF Ablation (iccc_p4_Im4.png)
im_cdf = Image.open(os.path.join(src_dir, "iccc_p4_Im4.png"))
im_cdf.save(os.path.join(dst_dir, "paper-iccc-cdf.png"), "PNG")
print("Saved paper-iccc-cdf.png:", im_cdf.size)

# 5. ICCC Paper - 4-Layer Radio Map (ToA, AoA, EoA, RSS) Composite
im_aoa = Image.open(os.path.join(src_dir, "iccc_p2_Im0.png"))
im_eoa = Image.open(os.path.join(src_dir, "iccc_p2_Im1.png"))
im_toa = Image.open(os.path.join(src_dir, "iccc_p2_Im2.png"))
im_rss = Image.open(os.path.join(src_dir, "iccc_p2_Im3.png"))

# Resize to shared size and build 2x2 grid
cell_w, cell_h = 700, 560
aoa_r = im_aoa.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
eoa_r = im_eoa.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
toa_r = im_toa.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
rss_r = im_rss.resize((cell_w, cell_h), Image.Resampling.LANCZOS)

comp_rm = Image.new("RGB", (cell_w * 2, cell_h * 2), (255, 255, 255))
comp_rm.paste(rss_r, (0, 0))
comp_rm.paste(toa_r, (cell_w, 0))
comp_rm.paste(aoa_r, (0, cell_h))
comp_rm.paste(eoa_r, (cell_w, cell_h))
comp_rm.save(os.path.join(dst_dir, "paper-iccc-radiomap.png"), "PNG")
print("Saved paper-iccc-radiomap.png:", comp_rm.size)

# 6. Project 3 - Radar SLAM Point Cloud Map (pptx_image19.png)
im_pointcloud = Image.open(os.path.join(src_dir, "pptx_image19.png"))
im_pointcloud.save(os.path.join(dst_dir, "project-radar-slam-map.png"), "PNG")
print("Saved project-radar-slam-map.png:", im_pointcloud.size)

# 7. Multi-sensor Smoke/Tunnel Experiment (pptx_image20.png)
im_multimodal = Image.open(os.path.join(src_dir, "pptx_image20.png"))
im_multimodal.save(os.path.join(dst_dir, "project-multimodal-perception.png"), "PNG")
print("Saved project-multimodal-perception.png:", im_multimodal.size)

print("All paper figures successfully prepared!")
