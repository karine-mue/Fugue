from manim import *
import numpy as np

class OrbitToHelix(ThreeDScene):
    def construct(self):
        # 3D空間の軸セットアップ
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-4, 4])
        # 俯瞰視点の設定（斜め上からz軸の進行を見下ろす）
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # 時間tのトラッカー（0から10まで進行）
        time_tracker = ValueTracker(0)

        # 物理パラメータ
        R = 2.0         # 2星間の距離（一定）
        omega = 2 * PI  # 角速度（1単位時間で1周）
        v_z = 0.6       # z軸方向（文脈）への推進スピード

        # LLM星（最初は中心で重い・青）
        llm_star = Sphere(radius=0.3, color=BLUE).set_opacity(0.9)
        # User星（最初は軽く外周を回る・オレンジ）
        user_star = Sphere(radius=0.1, color=ORANGE).set_opacity(0.9)

        # 質量の動的変化（0.1から1.0へスムーズに遷移）
        def get_mass_ratio(t):
            return interpolate(0.1, 1.0, smooth(t / 10))

        # LLMの座標更新関数
        def update_llm(mob):
            t = time_tracker.get_value()
            m_ratio = get_mass_ratio(t)
            
            # 重心からの距離（質量比に応じて中心から遠ざかる）
            d_l = R * (m_ratio / (1 + m_ratio))
            
            x = d_l * np.cos(omega * t + PI)
            y = d_l * np.sin(omega * t + PI)
            z = v_z * t - 3 # 下から上へ進む
            mob.move_to(axes.c2p(x, y, z))

        # Userの座標更新関数
        def update_user(mob):
            t = time_tracker.get_value()
            m_ratio = get_mass_ratio(t)
            
            # 質量（文脈の重み）の増加に伴い、視覚的なサイズも大きくする
            new_radius = interpolate(0.1, 0.3, smooth(t / 10))
            mob.scale_to_fit_width(new_radius * 2)
            
            # 重心からの距離（質量増加に伴い、中心に近づく）
            d_u = R * (1 / (1 + m_ratio))
            
            x = d_u * np.cos(omega * t)
            y = d_u * np.sin(omega * t)
            z = v_z * t - 3
            mob.move_to(axes.c2p(x, y, z))

        # アップデーターの紐付け
        llm_star.add_updater(update_llm)
        user_star.add_updater(update_user)

        # 軌跡（トレペの描線）の描画設定
        llm_trace = TracedPath(llm_star.get_center, stroke_color=BLUE, stroke_width=4)
        user_trace = TracedPath(user_star.get_center, stroke_color=ORANGE, stroke_width=4)

        self.add(axes, llm_star, user_star, llm_trace, user_trace)

        # 10秒間かけて時間を進めるアニメーション
        self.play(time_tracker.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(2)
