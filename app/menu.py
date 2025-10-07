def mostrar_menu_principal():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Resolver integral triple")
        print("2. Resolver integral de superficie")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n[ Módulo de integrales triples en construcción... ]")
            # Aquí luego llamaremos a integrales_triples.py
        elif opcion == "2":
            print("\n[ Módulo de integrales de superficie en construcción... ]")
            # Aquí luego llamaremos a integrales_superficie.py
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
