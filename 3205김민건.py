import streamlit as st
import math
import random

# 1. 페이지 및 스타일 설정
st.set_page_config(
    page_title="3205 김민건 - 스페이스 에코스",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Orbitron', sans-serif; }
    .main-title {
        background: linear-gradient(45deg, #00F2FE, #4FACFE, #00C6FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 2.6rem;
    }
</style>
""", unsafe_allow_html=True)

# 2. 게임 세션 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'minerals' not in st.session_state:
    st.session_state.minerals = 100
if 'base_hp' not in st.session_state:
    st.session_state.base_hp = 100
if 'power_level' not in st.session_state:
    st.session_state.power_level = 1
if 'turret_level' not in st.session_state:
    st.session_state.turret_level = 1
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'targets' not in st.session_state:
    st.session_state.targets = [
        {"id": 1, "type": "ore", "x": 60, "y": 45, "r": 6, "hp": 50, "max_hp": 50, "reward": 80, "name": "💎 티타늄 행성", "color": "#00F2FE"},
        {"id": 2, "type": "ore", "x": 85, "y": 25, "r": 8, "hp": 80, "max_hp": 80, "reward": 150, "name": "🌌 다이아몬드 코어", "color": "#9b59b6"},
        {"id": 3, "type": "enemy", "x": 75, "y": 60, "r": 5, "hp": 40, "max_hp": 40, "reward": 100, "name": "👾 외계 침략선", "color": "#ff4757"},
        {"id": 4, "type": "enemy", "x": 90, "y": 55, "r": 5, "hp": 60, "max_hp": 60, "reward": 120, "name": "🛸 모선 디스트로이어", "color": "#ffa502"}
    ]

def reset_game():
    st.session_state.score = 0
    st.session_state.minerals = 100
    st.session_state.base_hp = 100
    st.session_state.power_level = 1
    st.session_state.turret_level = 1
    st.session_state.attempts = 0
    st.session_state.targets = [
        {"id": 1, "type": "ore", "x": 60, "y": 45, "r": 6, "hp": 50, "max_hp": 50, "reward": 80, "name": "💎 티타늄 행성", "color": "#00F2FE"},
        {"id": 2, "type": "ore", "x": 85, "y": 25, "r": 8, "hp": 80, "max_hp": 80, "reward": 150, "name": "🌌 다이아몬드 코어", "color": "#9b59b6"},
        {"id": 3, "type": "enemy", "x": 75, "y": 60, "r": 5, "hp": 40, "max_hp": 40, "reward": 100, "name": "👾 외계 침략선", "color": "#ff4757"},
        {"id": 4, "type": "enemy", "x": 90, "y": 55, "r": 5, "hp": 60, "max_hp": 60, "reward": 120, "name": "🛸 모선 디스트로이어", "color": "#ffa502"}
    ]

# 3. 레이아웃 헤더
st.markdown("<h1 class='main-title'>🚀 SPACE ECHOES : 우주 채굴 & 방어</h1>", unsafe_allow_html=True)
st.write("3205 김민건 제작 | 물리 궤적 채굴 & 실시간 우주 방어 시뮬레이션")

# 4. 사이드바 (상점 및 대시보드)
st.sidebar.title("🎮 기지 통제실")
st.sidebar.write(f"👤 **사령관:** 3205 김민건")
st.sidebar.write(f"⭐ **현재 점수:** {st.session_state.score} PTS")
st.sidebar.write(f"💎 **보유 광물:** {st.session_state.minerals} Ore")
st.sidebar.write(f"🛡️ **기지 내구도:** {st.session_state.base_hp} / 100")

st.sidebar.divider()
st.sidebar.subheader("🛠️ 연구소 및 무기 강화")

cost_power = st.session_state.power_level * 50
if st.sidebar.button(f"⚡ 발사체 파워 Lv.{st.session_state.power_level + 1} ({cost_power} 광물)"):
    if st.session_state.minerals >= cost_power:
        st.session_state.minerals -= cost_power
        st.session_state.power_level += 1
        st.toast("⚡ 발사체 파워가 업그레이드되었습니다!", icon="🚀")
    else:
        st.sidebar.error("광물이 부족합니다!")

cost_turret = st.session_state.turret_level * 70
if st.sidebar.button(f"🛡️ 방어 포탑 Lv.{st.session_state.turret_level + 1} ({cost_turret} 광물)"):
    if st.session_state.minerals >= cost_turret:
        st.session_state.minerals -= cost_turret
        st.session_state.turret_level += 1
        st.toast("🛡️ 방어 포탑이 강화되었습니다!", icon="🛰️")
    else:
        st.sidebar.error("광물이 부족합니다!")

if st.sidebar.button("🔧 기지 수리 (+30 HP / 40 광물)"):
    if st.session_state.minerals >= 40:
        st.session_state.minerals -= 40
        st.session_state.base_hp = min(100, st.session_state.base_hp + 30)
        st.toast("🔧 기지가 수리되었습니다!", icon="🛠️")
    else:
        st.sidebar.error("광물이 부족합니다!")

st.sidebar.divider()
if st.sidebar.button("🔄 미션 재시작"):
    reset_game()
    st.rerun()

# 5. 메인 게임 컨트롤
col_ctrl, col_field = st.columns([1, 2])

with col_ctrl:
    st.subheader("🎯 플라즈마 포 발사 조종")
    angle = st.slider("📐 발사 각도 (°)", min_value=5, max_value=85, value=40)
    power = st.slider("💥 추력 파워", min_value=20, max_value=100, value=65)
    ammo_type = st.selectbox("💣 탄환 종류", [
        "🔵 관통형 플라즈마 (기본)",
        "💥 중력 폭탄 (광범위 타격)",
        "✨ 유도 입자탄 (명중률 증가)"
    ])
    planet_gravity = st.radio("🌌 지역 중력 환경", ["달 (저중력)", "지구 (표준)", "목성 (고중력)"], horizontal=True)
    
    launch_btn = st.button("🔥 플라즈마 발사!", use_container_width=True)

g_map = {"달 (저중력)": 4.0, "지구 (표준)": 9.8, "목성 (고중력)": 18.0}
g = g_map[planet_gravity]

trajectory_x, trajectory_y = [], []
hit_logs = []

if launch_btn and st.session_state.base_hp > 0:
    st.session_state.attempts += 1
    
    v_bonus = 1.0 + (st.session_state.power_level * 0.15)
    v0 = power * 0.85 * v_bonus
    rad = math.radians(angle)
    vx = v0 * math.cos(rad)
    vy = v0 * math.sin(rad)
    
    dt = 0.08
    t = 0
    damage = 25 * st.session_state.power_level
    if "중력 폭탄" in ammo_type:
        damage *= 1.4
        
    while t < 12:
        x = vx * t
        y = (vy * t) - (0.5 * g * (t ** 2))
        if y < 0:
            break
        
        trajectory_x.append(x)
        trajectory_y.append(y)
        
        for target in st.session_state.targets:
            if target["hp"] > 0:
                dist = math.sqrt((x - target["x"])**2 + (y - target["y"])**2)
                hit_radius = target["r"] + (4 if "중력 폭탄" in ammo_type else 2)
                
                if dist <= hit_radius:
                    target["hp"] -= damage
                    hit_logs.append(f"🎯 {target['name']}에 {int(damage)} 데미지!")
                    
                    if target["hp"] <= 0:
                        target["hp"] = 0
                        st.session_state.score += target["reward"]
                        st.session_state.minerals += target["reward"] // 2
                        hit_logs.append(f"💥 {target['name']} 파괴! +{target['reward']} PTS / +{target['reward']//2} 광물 획득")
                    break
        t += dt

    # 외계인 반격 시스템
    for target in st.session_state.targets:
        if target["type"] == "enemy" and target["hp"] > 0:
            if random.random() < 0.6:
                enemy_dmg = max(5, random.randint(10, 20) - (st.session_state.turret_level * 3))
                st.session_state.base_hp -= enemy_dmg
                hit_logs.append(f"⚠️ {target['name']}의 반격! 기지 피해 -{enemy_dmg} HP")

with col_field:
    st.subheader("🌌 우주 전장 뷰어 (SVG 파티클)")
    
    svg = f"""
    <svg viewBox="0 0 120 80" width="100%" height="420" style="background: #090A0F; border-radius: 12px; border: 1px solid #1E293B;">
        <defs>
            <radialGradient id="space-bg" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#1E1E38" />
                <stop offset="100%" stop-color="#090A0F" />
            </radialGradient>
        </defs>
        <rect width="120" height="80" fill="url(#space-bg)" />
        <rect x="0" y="65" width="120" height="15" fill="#1E293B" />
        <line x1="10" y1="65" x2="{10 + 10 * math.cos(math.radians(angle))}" y2="{65 - 10 * math.sin(math.radians(angle))}" stroke="#00F2FE" stroke-width="2.5" />
    """
    
    for target in st.session_state.targets:
        if target["hp"] > 0:
            hp_percent = target["hp"] / target["max_hp"]
            svg += f"""
            <circle cx="{target['x']}" cy="{70-target['y']}" r="{target['r']}" fill="{target['color']}" opacity="0.85"/>
            <rect x="{target['x']-6}" y="{70-target['y']-target['r']-4}" width="12" height="1.8" fill="#333"/>
            <rect x="{target['x']-6}" y="{70-target['y']-target['r']-4}" width="{12 * hp_percent}" height="1.8" fill="#2ed573"/>
            """
        else:
            svg += f'<text x="{target["x"]-3}" y="{70-target["y"]+2}" font-size="6">💥</text>'
            
    if trajectory_x:
        pts = " ".join([f"{x+10},{65-y}" for x, y in zip(trajectory_x, trajectory_y)])
        svg += f'<polyline points="{pts}" fill="none" stroke="#00F2FE" stroke-width="1" stroke-dasharray="2,1"/>'
        last_x = trajectory_x[-1] + 10
        last_y = 65 - trajectory_y[-1]
        svg += f'<circle cx="{last_x}" cy="{last_y}" r="2.5" fill="#FF4757"/>'
        
    svg += "</svg>"
    
    st.components.v1.html(svg, height=430)

    for log in hit_logs:
        if "파괴" in log or "획득" in log:
            st.success(log)
        elif "피해" in log:
            st.error(log)
        else:
            st.info(log)

# 6. 미션 성공 / 실패 처리
active_targets = [t for t in st.session_state.targets if t["hp"] > 0]
if len(active_targets) == 0:
    st.balloons()
    st.success(f"🏆 [MISSION COMPLETE] 모든 세력 제압 및 광물 채굴 완료! (총 점수: {st.session_state.score} PTS)")

if st.session_state.base_hp <= 0:
    st.error("💥 [GAME OVER] 기지가 파괴되었습니다! 사이드바에서 재시작을 눌러주세요.")
