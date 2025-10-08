# calculo.py
# Este archivo contiene toda la lógica para resolver las integrales.

import numpy as np
import sympy
from scipy.integrate import tplquad

def resolver_integral_triple(funcion_str, var_str, limites, coordenadas='rectangulares'):
    """
    Resuelve una integral triple numérica a partir de strings.

    Args:
        funcion_str (str): La función a integrar como texto (ej. "x*y + z").
        var_str (list): Lista de variables en orden de integración (ej. ['z', 'y', 'x']).
        limites (dict): Un diccionario con los límites para cada variable.
        coordenadas (str): El sistema de coordenadas ('rectangulares', 'cilindricas', 'esfericas').

    Returns:
        float: El resultado de la integral o un mensaje de error.
    """
    try:
        # 1. Definir los símbolos de las variables con SymPy
        x, y, z, r, theta, rho, phi = sympy.symbols('x y z r theta rho phi')
        
        # Mapeo de variables según el sistema de coordenadas
        mapa_vars = {
            'rectangulares': (x, y, z),
            'cilindricas': (r, theta, z),
            'esfericas': (rho, phi, theta)
        }
        
        # Símbolos para la función a evaluar (siempre son x, y, z)
        simbolos_func = {'x': x, 'y': y, 'z': z}

        # 2. Transformar la función de texto a una función numérica
        # El usuario escribe la función en términos de x, y, z
        expr_func = sympy.sympify(funcion_str, locals=simbolos_func)

        # Sustituir x, y, z por sus equivalentes en otras coordenadas si es necesario
        if coordenadas == 'cilindricas':
            expr_func = expr_func.subs({x: r * sympy.cos(theta), y: r * sympy.sin(theta)})
            # Añadir el Jacobiano r
            expr_func *= r
        elif coordenadas == 'esfericas':
            expr_func = expr_func.subs({
                x: rho * sympy.sin(phi) * sympy.cos(theta),
                y: rho * sympy.sin(phi) * sympy.sin(theta),
                z: rho * sympy.cos(phi)
            })
            # Añadir el Jacobiano rho^2 * sin(phi)
            expr_func *= rho**2 * sympy.sin(phi)

        # Convertir la expresión final a una función lambda para scipy
        variables_integracion = mapa_vars[coordenadas]
        func_numerica = sympy.lambdify(variables_integracion, expr_func, 'numpy')

        # 3. Preparar los límites de integración
        limites_finales = []
        for var_char in var_str: # ['z', 'y', 'x'] o el orden que sea
            lim_inf_str, lim_sup_str = limites[var_char]
            
            # Convierte los límites (que pueden ser funciones) a funciones lambda
            # El orden de los argumentos en lambdify es importante
            if var_char == var_str[0]: # Límite más interno
                lim_inf = sympy.lambdify(variables_integracion[1:], sympy.sympify(lim_inf_str), 'numpy')
                lim_sup = sympy.lambdify(variables_integracion[1:], sympy.sympify(lim_sup_str), 'numpy')
            elif var_char == var_str[1]: # Límite intermedio
                lim_inf = sympy.lambdify(variables_integracion[2:], sympy.sympify(lim_inf_str), 'numpy')
                lim_sup = sympy.lambdify(variables_integracion[2:], sympy.sympify(lim_sup_str), 'numpy')
            else: # Límite exterior (debe ser numérico)
                lim_inf = float(eval(lim_inf_str))
                lim_sup = float(eval(lim_sup_str))
            
            limites_finales.extend([lim_inf, lim_sup])

        # 4. Calcular la integral con tplquad de SciPy
        # El orden de los límites para tplquad es: [gfun, hfun, qfun, rfun, a, b]
        # que corresponde a: [y_inf, y_sup, z_inf, z_sup, x_inf, x_sup] si el orden es dy dz dx
        # Nuestra estructura es [z_inf, z_sup, y_inf, y_sup, x_inf, x_sup]
        # tplquad espera el orden de variables (x, y, z)
        resultado, error = tplquad(
            func_numerica,
            limites_finales[4], limites_finales[5], # Límites de x (o primera var)
            limites_finales[2], limites_finales[3], # Límites de y (o segunda var)
            limites_finales[0], limites_finales[1]  # Límites de z (o tercera var)
        )

        return resultado

    except Exception as e:
        # Captura cualquier error (sintaxis, etc.) y lo devuelve como mensaje
        print(e) # Imprime el error en consola para depuración
        return "Error en la expresión o los límites."