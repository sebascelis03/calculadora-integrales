# calculo.py

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

class MathBackend:
    def __init__(self):
        self.x, self.y, self.z = sp.symbols('x y z')
        self.r, self.theta = sp.symbols('r theta')
        self.rho, self.phi = sp.symbols('rho phi')

    def _parse_expression(self, expr_str):
        return sp.sympify(expr_str)

    def solve_triple_integral(self, func_str, limits, mode):
        try:
            if mode == "Rectangulares":
                return self._solve_rectangular(func_str, limits)
            elif mode == "Cilíndricas":
                return self._solve_cylindrical(func_str, limits)
            elif mode == "Esféricas":
                return self._solve_spherical(func_str, limits)
            else:
                return {"error": "Modo no soportado"}
        except Exception as e:
            return {"error": f"Error en el cálculo: {e}"}

    def _solve_rectangular(self, func_str, limits):
        f = self._parse_expression(func_str)
        lim_x = [self._parse_expression(l) for l in limits['x']]
        lim_y = [self._parse_expression(l) for l in limits['y']]
        lim_z = [self._parse_expression(l) for l in limits['z']]
        integral = sp.integrate(f, (self.z, lim_z[0], lim_z[1]), (self.y, lim_y[0], lim_y[1]), (self.x, lim_x[0], lim_x[1]))
        proceso = f"∫({lim_x[0]})→({lim_x[1]}) ∫({lim_y[0]})→({lim_y[1]}) ∫({lim_z[0]})→({lim_z[1]}) [{f}] dz dy dx"
        return {"proceso": proceso, "resultado_simbolico": str(integral), "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A"}

    def _solve_cylindrical(self, func_str, limits):
        f_rect = self._parse_expression(func_str)
        substitutions = {self.x: self.r * sp.cos(self.theta), self.y: self.r * sp.sin(self.theta)}
        f_cyl = f_rect.subs(substitutions)
        f_integrar = f_cyl * self.r
        lim_z = [self._parse_expression(l) for l in limits['z']]
        lim_r = [self._parse_expression(l) for l in limits['r']]
        lim_theta = [self._parse_expression(l) for l in limits['theta']]
        integral = sp.integrate(f_integrar, (self.z, lim_z[0], lim_z[1]), (self.r, lim_r[0], lim_r[1]), (self.theta, lim_theta[0], lim_theta[1]))
        proceso = f"∫({lim_theta[0]})→({lim_theta[1]}) ∫({lim_r[0]})→({lim_r[1]}) ∫({lim_z[0]})→({lim_z[1]}) [{f_cyl}] * r dz dr dθ"
        return {"proceso": proceso, "resultado_simbolico": str(integral), "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A"}

    def _solve_spherical(self, func_str, limits):
        f_rect = self._parse_expression(func_str)
        substitutions = {self.x: self.rho * sp.sin(self.phi) * sp.cos(self.theta), self.y: self.rho * sp.sin(self.phi) * sp.sin(self.theta), self.z: self.rho * sp.cos(self.phi)}
        f_sph = f_rect.subs(substitutions)
        f_integrar = f_sph * self.rho**2 * sp.sin(self.phi)
        lim_rho = [self._parse_expression(l) for l in limits['rho']]
        lim_phi = [self._parse_expression(l) for l in limits['phi']]
        lim_theta = [self._parse_expression(l) for l in limits['theta']]
        integral = sp.integrate(f_integrar, (self.rho, lim_rho[0], lim_rho[1]), (self.phi, lim_phi[0], lim_phi[1]), (self.theta, lim_theta[0], lim_theta[1]))
        proceso = f"∫({lim_theta[0]})→({lim_theta[1]}) ∫({lim_phi[0]})→({lim_phi[1]}) ∫({lim_rho[0]})→({lim_rho[1]}) [{f_sph}] * ρ²sin(φ) dρ dφ dθ"
        return {"proceso": proceso, "resultado_simbolico": str(integral), "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A"}

    def plot_rectangular_domain(self, limits):
        try:
            lim_x_expr = [self._parse_expression(l) for l in limits['x']]
            lim_y_expr = [self._parse_expression(l) for l in limits['y']]
            lim_z_expr = [self._parse_expression(l) for l in limits['z']]
            z_func_baja = sp.lambdify((self.x, self.y), lim_z_expr[0], 'numpy')
            z_func_alta = sp.lambdify((self.x, self.y), lim_z_expr[1], 'numpy')

            if not all(l.is_number for l in lim_x_expr): return None

            x_inf_num, x_sup_num = float(lim_x_expr[0]), float(lim_x_expr[1])
            x_range = np.linspace(x_inf_num, x_sup_num, 30)
            
            y_lower_func = sp.lambdify(self.x, lim_y_expr[0], 'numpy')
            y_upper_func = sp.lambdify(self.x, lim_y_expr[1], 'numpy')
            
            y_lower_bound = y_lower_func(x_range)
            y_upper_bound = y_upper_func(x_range)

            y_lower_bound = np.atleast_1d(y_lower_bound)
            y_upper_bound = np.atleast_1d(y_upper_bound)

            if y_lower_bound.size == 1:
                y_lower_bound = np.full_like(x_range, y_lower_bound[0])
            if y_upper_bound.size == 1:
                y_upper_bound = np.full_like(x_range, y_upper_bound[0])

            x_vals, y_vals = np.array([]), np.array([])
            for i in range(len(x_range)):
                x_val = x_range[i]
                y_start = y_lower_bound[i]
                y_end = y_upper_bound[i]
                y_range = np.linspace(y_start, y_end, 30)
                
                x_col = np.full_like(y_range, x_val)
                x_vals = np.concatenate([x_vals, x_col])
                y_vals = np.concatenate([y_vals, y_range])

            Z_baja, Z_alta = z_func_baja(x_vals, y_vals), z_func_alta(x_vals, y_vals)
            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_trisurf(x_vals, y_vals, Z_baja, cmap='winter', alpha=0.7)
            ax.plot_trisurf(x_vals, y_vals, Z_alta, cmap='viridis', alpha=0.7)
            ax.set_xlabel('Eje X'); ax.set_ylabel('Eje Y'); ax.set_zlabel('Eje Z')
            ax.set_title('Dominio de Integración Rectangular')
            return fig
        except Exception as e:
            print(f"Error al graficar (rectangular): {e}")
            return None

    def plot_cylindrical_domain(self, limits):
        try:
            lim_z_expr = [self._parse_expression(l) for l in limits['z']]
            lim_r_expr = [self._parse_expression(l) for l in limits['r']]
            lim_theta_expr = [self._parse_expression(l) for l in limits['theta']]
            z_func_baja = sp.lambdify((self.r, self.theta), lim_z_expr[0], 'numpy')
            z_func_alta = sp.lambdify((self.r, self.theta), lim_z_expr[1], 'numpy')
            r_inf, r_sup = float(lim_r_expr[0]), float(lim_r_expr[1])
            theta_inf, theta_sup = float(sp.sympify(lim_theta_expr[0]).evalf()), float(sp.sympify(lim_theta_expr[1]).evalf())
            R, THETA = np.meshgrid(np.linspace(r_inf, r_sup, 30), np.linspace(theta_inf, theta_sup, 30))
            X, Y = R * np.cos(THETA), R * np.sin(THETA)
            Z_baja, Z_alta = z_func_baja(R, THETA), z_func_alta(R, THETA)
            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z_baja, cmap='winter', alpha=0.6)
            ax.plot_surface(X, Y, Z_alta, cmap='viridis', alpha=0.6)
            ax.set_xlabel('Eje X'); ax.set_ylabel('Eje Y'); ax.set_zlabel('Eje Z')
            ax.set_title('Dominio de Integración Cilíndrico')
            return fig
        except Exception as e:
            print(f"Error al graficar (cilíndrico): {e}")
            return None

    def plot_spherical_domain(self, limits):
        try:
            lim_rho_expr = [self._parse_expression(l) for l in limits['rho']]
            lim_phi_expr = [self._parse_expression(l) for l in limits['phi']]
            lim_theta_expr = [self._parse_expression(l) for l in limits['theta']]
            rho_func = sp.lambdify((self.phi, self.theta), lim_rho_expr[1], 'numpy')
            phi_inf, phi_sup = float(sp.sympify(lim_phi_expr[0]).evalf()), float(sp.sympify(lim_phi_expr[1]).evalf())
            theta_inf, theta_sup = float(sp.sympify(lim_theta_expr[0]).evalf()), float(sp.sympify(lim_theta_expr[1]).evalf())
            PHI, THETA = np.meshgrid(np.linspace(phi_inf, phi_sup, 40), np.linspace(theta_inf, theta_sup, 40))
            RHO = rho_func(PHI, THETA)
            X, Y, Z = RHO * np.sin(PHI) * np.cos(THETA), RHO * np.sin(PHI) * np.sin(THETA), RHO * np.cos(PHI)
            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='magma', alpha=0.8)
            ax.set_xlabel('Eje X'); ax.set_ylabel('Eje Y'); ax.set_zlabel('Eje Z')
            ax.set_title('Dominio de Integración Esférico')
            return fig
        except Exception as e:
            print(f"Error al graficar (esférico): {e}")
            return None