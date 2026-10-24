import math
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BG_LIGHT = (238, 240, 243)
SURFACE = (226, 229, 234)
INK_DARK = (11, 12, 14)
MUTED = (82, 88, 102)
ACCENT_BLUE = (31, 45, 230)
ACCENT_LIGHT = (210, 220, 255)
WHITE = (255, 255, 255)

def get_font(size):
    try:
        # macOS default fonts
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        return ImageFont.load_default()

def create_radar_slam_figure():
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    
    # Border / panel
    draw.rectangle([40, 40, W-40, H-40], fill=WHITE, outline=SURFACE, width=2)
    
    # Title & Subtitle
    font_title = get_font(28)
    font_sub = get_font(18)
    font_small = get_font(14)
    
    draw.text((80, 70), "MMW Radar SLAM: Coordinate Transformation & Error Compensation", fill=INK_DARK, font=font_title)
    draw.text((80, 110), "CEEC-CSM Cumulative Error Expectation Compensation · IEEE TIM Vol. 74", fill=MUTED, font=font_sub)
    
    # Left: Radar Polar Sweep Frame
    cx, cy = 340, 440
    r_max = 240
    for r in range(60, r_max + 1, 60):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=SURFACE, width=1)
        draw.text((cx + 10, cy - r - 12), f"{r//3}m", fill=MUTED, font=font_small)
    
    # Radial lines
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x2 = cx + int(r_max * math.cos(rad))
        y2 = cy + int(r_max * math.sin(rad))
        draw.line([cx, cy, x2, y2], fill=SURFACE, width=1)
    
    # Sensor beam angle
    draw.pieslice([cx - r_max, cy - r_max, cx + r_max, cy + r_max], 250, 290, fill=(230, 235, 255, 128), outline=ACCENT_BLUE, width=2)
    draw.line([cx, cy, cx, cy - r_max], fill=ACCENT_BLUE, width=2)
    draw.text((cx - 30, cy + 10), "Sensor O_B", fill=INK_DARK, font=font_small)
    
    # Point cloud clusters (raw observation)
    import random
    random.seed(42)
    for _ in range(80):
        dist = random.uniform(80, 230)
        ang = math.radians(random.uniform(252, 288))
        px = cx + int(dist * math.cos(ang)) + random.randint(-4, 4)
        py = cy + int(dist * math.sin(ang)) + random.randint(-4, 4)
        draw.ellipse([px-3, py-3, px+3, py+3], fill=ACCENT_BLUE)
        
    # Right: Trajectory Comparison
    tx_start, ty_start = 680, 180
    draw.rectangle([tx_start, ty_start, W-80, H-80], fill=BG_LIGHT)
    draw.text((tx_start + 30, ty_start + 25), "Trajectory Drift & Correction (49% Error Reduction)", fill=INK_DARK, font=font_sub)
    
    # Grid lines
    for gy in range(ty_start + 70, H - 120, 50):
        draw.line([tx_start + 30, gy, W - 110, gy], fill=SURFACE, width=1)
    for gx in range(tx_start + 30, W - 110, 60):
        draw.line([gx, ty_start + 70, gx, H - 120], fill=SURFACE, width=1)
        
    # Ground Truth Path (Dark line)
    gt_pts = []
    for i in range(15):
        x = tx_start + 60 + i * 26
        y = ty_start + 360 - int(math.sin(i * 0.4) * 110) - i * 12
        gt_pts.append((x, y))
    draw.line(gt_pts, fill=INK_DARK, width=3)
    
    # Uncompensated CSM Path (Red dashed drift)
    csm_pts = []
    for i, (gx, gy) in enumerate(gt_pts):
        drift_x = gx + int(i * 3.8)
        drift_y = gy + int(i * i * 0.5)
        csm_pts.append((drift_x, drift_y))
    for i in range(len(csm_pts)-1):
        if i % 2 == 0:
            draw.line([csm_pts[i], csm_pts[i+1]], fill=(220, 40, 40), width=2)
            
    # Compensated CEEC-CSM Path (Cobalt blue)
    ceec_pts = []
    for i, (gx, gy) in enumerate(gt_pts):
        corr_x = gx + int(i * 0.6)
        corr_y = gy + int(i * 0.8)
        ceec_pts.append((corr_x, corr_y))
    draw.line(ceec_pts, fill=ACCENT_BLUE, width=3)
    
    # Legend
    draw.line([tx_start + 40, H - 100, tx_start + 80, H - 100], fill=INK_DARK, width=3)
    draw.text((tx_start + 90, H - 108), "Ground Truth", fill=INK_DARK, font=font_small)
    
    draw.line([tx_start + 200, H - 100, tx_start + 240, H - 100], fill=(220, 40, 40), width=2)
    draw.text((tx_start + 250, H - 108), "Standard CSM (Drift)", fill=INK_DARK, font=font_small)
    
    draw.line([tx_start + 370, H - 100, tx_start + 410, H - 100], fill=ACCENT_BLUE, width=3)
    draw.text((tx_start + 420, H - 108), "CEEC-CSM (-49% Error)", fill=ACCENT_BLUE, font=font_small)
    
    img.save("/Volumes/disk2/CV/assets/figure-radar-slam.png", "PNG")
    print("Saved figure-radar-slam.png")

def create_radio_map_figure():
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, W-40, H-40], fill=WHITE, outline=SURFACE, width=2)
    
    font_title = get_font(28)
    font_sub = get_font(18)
    font_small = get_font(14)
    
    draw.text((80, 70), "Small-Scale Radio Map NLoS Multipath Localization", fill=INK_DARK, font=font_title)
    draw.text((80, 110), "Ray-Tracing Simulation · AoA, ToA & RSS Feature Fingerprinting · IEEE/CIC ICCC 2026", fill=MUTED, font=font_sub)
    
    # 3D Urban Canyon Buildings (Isometric view)
    # Street floor
    floor_poly = [(200, 680), (600, 360), (1050, 360), (650, 680)]
    draw.polygon(floor_poly, fill=BG_LIGHT, outline=SURFACE)
    
    # Left Building block
    b1_pts = [(120, 620), (320, 460), (320, 200), (120, 360)]
    draw.polygon(b1_pts, fill=(215, 220, 228), outline=MUTED)
    b1_top = [(120, 360), (320, 200), (480, 200), (280, 360)]
    draw.polygon(b1_top, fill=(235, 238, 242), outline=MUTED)
    
    # Right Building block
    b2_pts = [(700, 620), (950, 420), (950, 160), (700, 360)]
    draw.polygon(b2_pts, fill=(215, 220, 228), outline=MUTED)
    b2_top = [(700, 360), (950, 160), (1080, 160), (830, 360)]
    draw.polygon(b2_top, fill=(235, 238, 242), outline=MUTED)
    
    # Transmitter (BS) on Right Building roof
    bs_pos = (960, 160)
    draw.ellipse([bs_pos[0]-8, bs_pos[1]-8, bs_pos[0]+8, bs_pos[1]+8], fill=ACCENT_BLUE)
    draw.text((bs_pos[0]-110, bs_pos[1]-28), "Base Station (Tx)", fill=ACCENT_BLUE, font=font_sub)
    
    # Receiver (MS) in street canyon (NLoS)
    ms_pos = (440, 580)
    draw.ellipse([ms_pos[0]-8, ms_pos[1]-8, ms_pos[0]+8, ms_pos[1]+8], fill=(220, 40, 40))
    draw.text((ms_pos[0]+15, ms_pos[1]-5), "Mobile Terminal (Rx, NLoS)", fill=(220, 40, 40), font=font_sub)
    
    # Direct Line of Sight (Blocked)
    draw.line([bs_pos, ms_pos], fill=(180, 180, 180), width=2)
    draw.text((680, 390), "× LoS Path Blocked", fill=(180, 180, 180), font=font_small)
    
    # Multipath Ray 1 (Reflection on left facade)
    ref1 = (280, 390)
    draw.line([bs_pos, ref1], fill=ACCENT_BLUE, width=3)
    draw.line([ref1, ms_pos], fill=ACCENT_BLUE, width=3)
    draw.ellipse([ref1[0]-5, ref1[1]-5, ref1[0]+5, ref1[1]+5], fill=ACCENT_BLUE)
    draw.text((ref1[0]-140, ref1[1]-10), "Reflection Point 1", fill=INK_DARK, font=font_small)
    
    # Multipath Ray 2 (Reflection on right facade)
    ref2 = (780, 480)
    draw.line([bs_pos, ref2], fill=(60, 150, 230), width=2)
    draw.line([ref2, ms_pos], fill=(60, 150, 230), width=2)
    draw.ellipse([ref2[0]-4, ref2[1]-4, ref2[0]+4, ref2[1]+4], fill=(60, 150, 230))
    
    # Multipath Ray 3 (Diffraction)
    ref3 = (320, 200)
    draw.line([bs_pos, ref3], fill=(100, 180, 100), width=2)
    draw.line([ref3, ms_pos], fill=(100, 180, 100), width=2)
    
    # Bottom Infographic Card
    draw.rectangle([80, H-120, W-80, H-60], fill=SURFACE)
    draw.text((100, H-102), "Key Research Finding:", fill=INK_DARK, font=font_sub)
    draw.text((320, H-102), "Azimuth AoA and Time Delay (ToA) provide dominant localization gain; RSS alone is insufficient.", fill=MUTED, font=font_sub)
    
    img.save("/Volumes/disk2/CV/assets/figure-radio-map.png", "PNG")
    print("Saved figure-radio-map.png")

def create_bev_reconstruction_figure():
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, W-40, H-40], fill=WHITE, outline=SURFACE, width=2)
    
    font_title = get_font(28)
    font_sub = get_font(18)
    font_small = get_font(14)
    
    draw.text((80, 70), "Urban Underground Road Panoramic Monitoring System", fill=INK_DARK, font=font_title)
    draw.text((80, 110), "Front & Side Radar SLAM Deployment · Large-Field Bird's Eye View (BEV) Fusion", fill=MUTED, font=font_sub)
    
    # Underground tunnel roadway (two-lane perspective)
    # BEV Roadway Grid
    rw_l = 100
    rw_r = W - 100
    rw_t = 180
    rw_b = H - 80
    draw.rectangle([rw_l, rw_t, rw_r, rw_b], fill=INK_DARK)
    
    # Tunnel side walls
    draw.rectangle([rw_l, rw_t, rw_l + 40, rw_b], fill=(45, 52, 65))
    draw.rectangle([rw_r - 40, rw_t, rw_r, rw_b], fill=(45, 52, 65))
    
    # Lane center dashed line
    mid_x = (rw_l + rw_r) // 2
    for y in range(rw_t + 20, rw_b, 50):
        draw.line([mid_x, y, mid_x, y + 25], fill=(240, 240, 240), width=4)
        
    # Ego vehicle with Dual Radars
    ego_x = mid_x - 140
    ego_y = 520
    draw.rectangle([ego_x - 30, ego_y - 60, ego_x + 30, ego_y + 60], fill=(220, 225, 235), outline=WHITE, width=2)
    draw.text((ego_x - 22, ego_y - 10), "EGO", fill=INK_DARK, font=font_small)
    
    # Front Radar FOV (Cobalt cone)
    draw.polygon([(ego_x, ego_y - 60), (ego_x - 160, ego_y - 300), (ego_x + 160, ego_y - 300)], fill=(31, 45, 230, 90), outline=ACCENT_BLUE)
    draw.text((ego_x - 60, ego_y - 220), "Front Radar FOV", fill=WHITE, font=font_small)
    
    # Side Radar FOV (Side cone toward tunnel wall)
    draw.polygon([(ego_x + 30, ego_y), (ego_x + 280, ego_y - 140), (ego_x + 280, ego_y + 140)], fill=(30, 180, 150, 90), outline=(30, 180, 150))
    draw.text((ego_x + 90, ego_y - 10), "Side Radar FOV", fill=WHITE, font=font_small)
    
    # Detected Obstacles / Vehicles in tunnel
    obs_x, obs_y = mid_x - 140, 260
    draw.rectangle([obs_x - 28, obs_y - 50, obs_x + 28, obs_y + 50], fill=(220, 50, 50), outline=WHITE, width=2)
    draw.text((obs_x - 24, obs_y - 10), "Target", fill=WHITE, font=font_small)
    
    obs2_x, obs2_y = mid_x + 140, 380
    draw.rectangle([obs2_x - 28, obs2_y - 50, obs2_x + 28, obs2_y + 50], fill=(220, 50, 50), outline=WHITE, width=2)
    draw.text((obs2_x - 24, obs2_y - 10), "Target", fill=WHITE, font=font_small)
    
    # Feature points along tunnel walls
    import random
    random.seed(99)
    for _ in range(120):
        py = random.randint(rw_t + 10, rw_b - 10)
        px1 = rw_l + 40 + random.randint(0, 15)
        px2 = rw_r - 40 - random.randint(0, 15)
        draw.ellipse([px1-2, py-2, px1+2, py+2], fill=ACCENT_LIGHT)
        draw.ellipse([px2-2, py-2, px2+2, py+2], fill=ACCENT_LIGHT)
        
    img.save("/Volumes/disk2/CV/assets/figure-bev-reconstruction.png", "PNG")
    print("Saved figure-bev-reconstruction.png")

def create_lab_context_figure():
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), (15, 18, 22))
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(32)
    font_sub = get_font(20)
    font_small = get_font(14)
    
    # Modern computational architecture / scientific research institute geometry
    # Shenzhen Peng Cheng & Xidian National Key Labs inspiration
    # Clean angular facade lines and glass atrium
    draw.polygon([(0, H), (450, 220), (750, 220), (1200, H)], fill=(24, 28, 36))
    
    # Structural columns and glass panes
    for x in range(100, 1100, 90):
        tx = int(450 + (x - 100) / 1000 * 300)
        draw.line([x, H, tx, 220], fill=(42, 48, 62), width=2)
        
    for y in range(260, H, 70):
        left_x = int((y - 220) / (H - 220) * -450 + 450)
        right_x = int((y - 220) / (H - 220) * 450 + 750)
        draw.line([left_x, y, right_x, y], fill=(36, 42, 54), width=1)
        
    # Horizon light line
    draw.line([0, 220, W, 220], fill=ACCENT_BLUE, width=2)
    
    # Overlay Title Card
    draw.rectangle([80, 80, 720, 200], fill=(11, 12, 14, 220))
    draw.text((110, 105), "Peng Cheng Laboratory & Xidian University", fill=WHITE, font=font_title)
    draw.text((110, 155), "Research Facilities · Spatial Computing & Wireless Communication Hubs", fill=(180, 190, 205), font=font_sub)
    
    img.save("/Volumes/disk2/CV/assets/lab-context.png", "PNG")
    print("Saved lab-context.png")

def create_radar_video_loop():
    W, H = 640, 480
    fps = 30
    duration = 2.0
    total_frames = int(fps * duration)
    
    frame_dir = "/Volumes/disk2/CV/assets/frames"
    os.makedirs(frame_dir, exist_ok=True)
    
    font = get_font(12)
    cx, cy = W // 2, H // 2
    r_max = 200
    
    for i in range(total_frames):
        img = Image.new("RGB", (W, H), (11, 12, 14))
        draw = ImageDraw.Draw(img)
        
        # Grid rings
        for r in range(50, r_max + 1, 50):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(35, 42, 55), width=1)
            
        # Axes
        draw.line([cx - r_max, cy, cx + r_max, cy], fill=(35, 42, 55), width=1)
        draw.line([cx, cy - r_max, cx, cy + r_max], fill=(35, 42, 55), width=1)
        
        # Sweep angle
        sweep_deg = (i / total_frames) * 360.0
        
        # Radar scan trail (sector gradient)
        for trail_step in range(30):
            t_deg = sweep_deg - trail_step * 1.5
            rad = math.radians(t_deg)
            tx = cx + int(r_max * math.cos(rad))
            ty = cy + int(r_max * math.sin(rad))
            alpha = int(255 * (1.0 - trail_step / 30.0))
            color = (int(31 * alpha / 255), int(45 * alpha / 255), int(230 * alpha / 255))
            draw.line([cx, cy, tx, ty], fill=color, width=2)
            
        # Leading beam
        lead_rad = math.radians(sweep_deg)
        lx = cx + int(r_max * math.cos(lead_rad))
        ly = cy + int(r_max * math.sin(lead_rad))
        draw.line([cx, cy, lx, ly], fill=(220, 235, 255), width=2)
        
        # Blips
        blips = [
            (cx + 80, cy - 60, 40),
            (cx - 110, cy - 90, 140),
            (cx + 120, cy + 80, 290),
            (cx - 70, cy + 120, 210)
        ]
        for bx, by, bang in blips:
            angle_diff = (sweep_deg - bang) % 360
            if angle_diff < 90:
                decay = 1.0 - (angle_diff / 90.0)
                b_color = (int(255 * decay), int(255 * decay), int(255 * decay))
                draw.ellipse([bx-4, by-4, bx+4, by+4], fill=b_color)
                
        draw.text((20, 20), "MMW SENSOR LIVE FEED", fill=(140, 150, 170), font=font)
        draw.text((20, 38), f"AZIMUTH: {int(sweep_deg)}°  SCAN: ACTIVE", fill=ACCENT_BLUE, font=font)
        
        img.save(f"{frame_dir}/frame_{i:03d}.png", "PNG")
        
    # Use ffmpeg to encode mp4
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", f"{frame_dir}/frame_%03d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "/Volumes/disk2/CV/assets/radar-loop.mp4"
    ]
    subprocess.run(cmd, check=True)
    print("Generated radar-loop.mp4")
    # Clean up frames
    for f in os.listdir(frame_dir):
        os.remove(os.path.join(frame_dir, f))
    os.rmdir(frame_dir)

if __name__ == "__main__":
    create_radar_slam_figure()
    create_radio_map_figure()
    create_bev_reconstruction_figure()
    create_lab_context_figure()
    create_radar_video_loop()
