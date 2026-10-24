// ==========================================================================
// Stephen Zhu · Academic Portfolio Scripts
// Interactive Features:
// 1. Work filter (All / Papers / Projects)
// 2. Interactive SLAM Coordinate & Error Compensation Instrument (The Live Thing)
// 3. Staggered reveal & motion observer
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  initWorkFilters();
  initSlamInstrument();
  initMotionLayer();
});

// 1. Work / Publication Filters
function initWorkFilters() {
  const filterBtns = document.querySelectorAll(".filter-btn");
  const workCards = document.querySelectorAll(".work-card");

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const filterType = btn.dataset.filter;
      workCards.forEach((card) => {
        if (filterType === "all" || card.dataset.type === filterType) {
          card.style.display = "grid";
          card.classList.add("is-visible");
        } else {
          card.style.display = "none";
        }
      });
    });
  });
}

// 2. Interactive SLAM Coordinate & Error Compensation Instrument
function initSlamInstrument() {
  const toggleRaw = document.getElementById("toggle-raw");
  const toggleCeec = document.getElementById("toggle-ceec");
  const angleSlider = document.getElementById("slider-angle");
  const angleReadout = document.getElementById("angle-readout");
  const errorReadout = document.getElementById("metric-error");
  const driftReadout = document.getElementById("metric-drift");
  const reductionReadout = document.getElementById("metric-reduction");
  const svgCanvas = document.getElementById("slam-svg-canvas");

  if (!svgCanvas || !angleSlider) return;

  let mode = "ceec"; // "raw" or "ceec"
  let angleDev = parseFloat(angleSlider.value) || 5; // degrees

  function updateSimulation() {
    angleDev = parseFloat(angleSlider.value);
    if (angleReadout) {
      angleReadout.textContent = `${angleDev.toFixed(1)}°`;
    }

    // Calculations based on IEEE TIM 2025 CEEC-CSM paper findings:
    // Raw CSM cumulative error scales quadratically with angular deviation
    const baseError = 0.25 + (angleDev / 15) * 1.25; // meters
    const rawError = baseError * 1.95;
    const ceecError = baseError;
    const reductionPercent = 49.1;

    if (mode === "raw") {
      errorReadout.textContent = `${rawError.toFixed(2)} m`;
      driftReadout.textContent = `沿变换轴方向累积 (+${(angleDev * 2.8).toFixed(1)} cm/步)`;
      reductionReadout.textContent = "未校正 (0%)";
      reductionReadout.classList.remove("metric-highlight");
    } else {
      errorReadout.textContent = `${ceecError.toFixed(2)} m`;
      driftReadout.textContent = "期望误差完全对称补偿";
      reductionReadout.textContent = `降低约 ${reductionPercent}%`;
      reductionReadout.classList.add("metric-highlight");
    }

    renderSvgScene(angleDev, mode);
  }

  function renderSvgScene(angle, currentMode) {
    const W = 700;
    const H = 400;

    // Center origin
    const ox = 120;
    const oy = 280;

    // Ground truth trajectory points
    const steps = 14;
    const stepDx = 38;
    const gtPts = [];
    for (let i = 0; i < steps; i++) {
      const x = ox + i * stepDx;
      const y = oy - Math.sin(i * 0.35) * 80 - i * 4;
      gtPts.push({ x, y });
    }

    // Estimated path
    const estPts = [];
    for (let i = 0; i < steps; i++) {
      const gt = gtPts[i];
      if (currentMode === "raw") {
        // Drift scales with step count and angle deviation
        const drift = (i * i * 0.42) * (angle / 6.0);
        estPts.push({ x: gt.x + (i * 1.5), y: gt.y + drift });
      } else {
        // CEEC-CSM compensated: tightly centered around GT
        const noise = Math.sin(i * 1.8) * 3;
        estPts.push({ x: gt.x + (i * 0.2) + noise, y: gt.y + noise });
      }
    }

    let gtPathD = `M ${gtPts[0].x} ${gtPts[0].y}`;
    for (let i = 1; i < gtPts.length; i++) {
      gtPathD += ` L ${gtPts[i].x} ${gtPts[i].y}`;
    }

    let estPathD = `M ${estPts[0].x} ${estPts[0].y}`;
    for (let i = 1; i < estPts.length; i++) {
      estPathD += ` L ${estPts[i].x} ${estPts[i].y}`;
    }

    const estColor = currentMode === "raw" ? "#cf222e" : "#1f2de6";
    const estDash = currentMode === "raw" ? "6,4" : "none";

    // Sensor beam projection from last point
    const lastEst = estPts[estPts.length - 1];
    const beamAngleRad = (angle - 25) * Math.PI / 180;
    const bx1 = lastEst.x + Math.cos(beamAngleRad - 0.25) * 70;
    const by1 = lastEst.y + Math.sin(beamAngleRad - 0.25) * 70;
    const bx2 = lastEst.x + Math.cos(beamAngleRad + 0.25) * 70;
    const by2 = lastEst.y + Math.sin(beamAngleRad + 0.25) * 70;

    let svgHtml = `
      <svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; overflow:visible;">
        <!-- Coordinate Grid -->
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#eef0f3" stroke-width="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Origin Frame -->
        <line x1="${ox}" y1="${oy}" x2="${ox + 50}" y2="${oy}" stroke="#525866" stroke-width="2"/>
        <line x1="${ox}" y1="${oy}" x2="${ox}" y2="${oy - 50}" stroke="#525866" stroke-width="2"/>
        <text x="${ox + 55}" y="${oy + 4}" font-size="12" fill="#525866" font-family="sans-serif">X_W</text>
        <text x="${ox - 6}" y="${oy - 58}" font-size="12" fill="#525866" font-family="sans-serif">Y_W</text>

        <!-- Ground Truth Path -->
        <path d="${gtPathD}" fill="none" stroke="#0b0c0e" stroke-width="3" />
        
        <!-- Estimated Path -->
        <path d="${estPathD}" fill="none" stroke="${estColor}" stroke-width="3" stroke-dasharray="${estDash}" />

        <!-- Sensor FOV cone at vehicle current pose -->
        <polygon points="${lastEst.x},${lastEst.y} ${bx1},${by1} ${bx2},${by2}" fill="${currentMode === 'raw' ? 'rgba(207,34,46,0.18)' : 'rgba(31,45,230,0.18)'}" stroke="${estColor}" stroke-width="1.5" />

        <!-- Vehicle Indicator -->
        <circle cx="${lastEst.x}" cy="${lastEst.y}" r="6" fill="${estColor}" stroke="#ffffff" stroke-width="2" />

        <!-- Labels & Legend inside canvas -->
        <rect x="40" y="24" width="280" height="68" fill="#eef0f3" />
        <line x1="56" y1="46" x2="86" y2="46" stroke="#0b0c0e" stroke-width="3"/>
        <text x="96" y="50" font-size="12" font-weight="600" fill="#0b0c0e" font-family="sans-serif">真实轨迹 (Ground Truth)</text>
        
        <line x1="56" y1="68" x2="86" y2="68" stroke="${estColor}" stroke-width="3" stroke-dasharray="${estDash}"/>
        <text x="96" y="72" font-size="12" font-weight="600" fill="${estColor}" font-family="sans-serif">
          ${currentMode === "raw" ? "标准 CSM (累积漂移)" : "CEEC-CSM (期望校准 -49%)"}
        </text>
      </svg>
    `;

    svgCanvas.innerHTML = svgHtml;
  }

  toggleRaw.addEventListener("click", () => {
    mode = "raw";
    toggleRaw.classList.add("active");
    toggleCeec.classList.remove("active");
    updateSimulation();
  });

  toggleCeec.addEventListener("click", () => {
    mode = "ceec";
    toggleCeec.classList.add("active");
    toggleRaw.classList.remove("active");
    updateSimulation();
  });

  angleSlider.addEventListener("input", updateSimulation);

  // Initial draw
  updateSimulation();
}

// 3. Motion Layer (Staggered Entrance & Shutter)
function initMotionLayer() {
  const animatedElements = document.querySelectorAll(".fade-up-item, .shutter-reveal");

  if (!("IntersectionObserver" in window)) {
    animatedElements.forEach((el) => {
      el.classList.add("is-visible");
      el.classList.add("is-revealed");
    });
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          entry.target.classList.add("is-revealed");
          obs.unobserve(entry.target);
        }
      });
    },
    {
      root: null,
      threshold: 0.1,
      rootMargin: "0px 0px -40px 0px",
    }
  );

  animatedElements.forEach((el) => observer.observe(el));
}
