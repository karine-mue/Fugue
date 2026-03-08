from manim import *
import numpy as np

class SazaedoLoop(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-3,3], y_range=[-3,3], z_range=[-4,4])
        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES)

        time_tracker = ValueTracker(0)

        R       = 2.0
        omega   = 0.8 * PI
        period  = 10
        z_amp   = 3

        def get_mass_ratio(t):
            phase    = (t % period) / period
            triangle = 2 * abs(phase - 0.5)
            return interpolate(0.1, 1.0, smooth(triangle))

        def get_z(t):
            return z_amp * np.sin(2 * PI * t / period)

        alpha = Sphere(radius=0.2, color=BLUE).set_opacity(0.9)
        beta  = Sphere(radius=0.2, color=ORANGE).set_opacity(0.9)

        def update_alpha(mob):
            t = time_tracker.get_value()
            m = get_mass_ratio(t)
            phase = omega * t  # 常に一定の角速度で回り続けるだけ
            d = R * m / (1 + m)
            mob.move_to(axes.c2p(
                d * np.cos(phase + PI),
                d * np.sin(phase + PI),
                get_z(t)
            ))

        def update_beta(mob):
            t = time_tracker.get_value()
            m = get_mass_ratio(t)
            phase = omega * t  # 常に一定の角速度で回り続けるだけ
            d = R / (1 + m)
            mob.move_to(axes.c2p(
                d * np.cos(phase),
                d * np.sin(phase),
                get_z(t)
            ))

        update_alpha(alpha)
        update_beta(beta)

        alpha.add_updater(update_alpha)
        beta.add_updater(update_beta)

        # 過去の文脈（軌跡）は5秒で減衰して消える
        alpha_trace = TracedPath(
            alpha.get_center,
            stroke_color=BLUE,
            stroke_width=4,
            dissipating_time=5
        )
        beta_trace = TracedPath(
            beta.get_center,
            stroke_color=ORANGE,
            stroke_width=4,
            dissipating_time=5
        )

        labels = axes.get_axis_labels(
            x_label="x", y_label="y",
            z_label=Text("文脈(z)", font_size=24)
        )

        self.add(axes, labels, alpha, beta, alpha_trace, beta_trace)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.play(
            time_tracker.animate.set_value(40),
            run_time=40,
            rate_func=linear
        )
        self.stop_ambient_camera_rotation()
        self.wait(2)