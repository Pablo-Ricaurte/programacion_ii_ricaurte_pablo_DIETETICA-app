from datetime import date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from consultorio.models import (
    Paciente,
    Nutricionista,
    Alimento,
    PlanNutricional,
    Consulta,
)
from consultorio.permissions_setup import configurar_grupos_y_permisos


class Command(BaseCommand):
    help = 'Crea grupos, permisos, usuarios de prueba y datos semilla para el consultorio de dietética.'

    def handle(self, *args, **options):
        grupo_admin, grupo_consultores = configurar_grupos_y_permisos()
        self.stdout.write(self.style.SUCCESS('1. Grupos "administradores" y "consultores" configurados.'))

        # 1. Superusuario
        superusuario, creado = User.objects.get_or_create(
            username='admin_ute',
            defaults={
                'email': 'admin.ute@consultorio.ec',
                'first_name': 'Pablo',
                'last_name': 'Ricaurte',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        superusuario.set_password('AdminUte2026*')
        superusuario.save()

        # 2. Usuario Administrador (grupo administradores)
        user_admin, _ = User.objects.get_or_create(
            username='laura_admin',
            defaults={
                'email': 'laura.admin@consultorio.ec',
                'first_name': 'Laura',
                'last_name': 'Vásquez',
                'is_staff': True,
            },
        )
        user_admin.set_password('NutriAdmin2026*')
        user_admin.save()
        user_admin.groups.set([grupo_admin])

        # 3. Usuario Consultor principal (grupo consultores)
        user_consultor, _ = User.objects.get_or_create(
            username='carlos_consultor',
            defaults={
                'email': 'carlos.consultor@consultorio.ec',
                'first_name': 'Carlos',
                'last_name': 'Mendoza',
            },
        )
        user_consultor.set_password('Consultor2026*')
        user_consultor.save()
        user_consultor.groups.set([grupo_consultores])

        # 4. Segundo Consultor (para comprobar regla de propiedad entre consultores)
        user_consultora2, _ = User.objects.get_or_create(
            username='ana_consultora',
            defaults={
                'email': 'ana.consultora@consultorio.ec',
                'first_name': 'Ana',
                'last_name': 'Torres',
            },
        )
        user_consultora2.set_password('Consultor2026*')
        user_consultora2.save()
        user_consultora2.groups.set([grupo_consultores])

        self.stdout.write(self.style.SUCCESS('2. Usuarios de prueba creados (admin_ute, laura_admin, carlos_consultor, ana_consultora).'))

        # 5 Nutricionistas
        datos_nutricionistas = [
            ('MSP-NUT-001', 'Valeria', 'Cárdenas', Nutricionista.Especialidad.CLINICA, '0991112233', 'valeria.cardenas@nutrivida.ec', True),
            ('MSP-NUT-002', 'Sebastián', 'Paredes', Nutricionista.Especialidad.DEPORTIVA, '0992223344', 'sebastian.paredes@nutrivida.ec', True),
            ('MSP-NUT-003', 'Camila', 'Salazar', Nutricionista.Especialidad.CONTROL_PESO, '0993334455', 'camila.salazar@nutrivida.ec', True),
            ('MSP-NUT-004', 'Mateo', 'Benítez', Nutricionista.Especialidad.PEDIATRICA, '0994445566', 'mateo.benitez@nutrivida.ec', True),
            ('MSP-NUT-005', 'Gabriela', 'Morales', Nutricionista.Especialidad.CLINICA, '0995556677', 'gabriela.morales@nutrivida.ec', False),
        ]
        nutricionistas = []
        for reg, nom, ape, esp, tel, mail, act in datos_nutricionistas:
            obj, _ = Nutricionista.objects.update_or_create(
                registro_profesional=reg,
                defaults={
                    'nombres': nom,
                    'apellidos': ape,
                    'especialidad': esp,
                    'telefono': tel,
                    'email': mail,
                    'activo': act,
                },
            )
            nutricionistas.append(obj)

        # 6 Alimentos
        datos_alimentos = [
            ('Pechuga de pollo a la plancha', Alimento.GrupoAlimenticio.PROTEINAS, 100, Decimal('165.00'), Decimal('31.00'), Decimal('0.00'), Decimal('3.60')),
            ('Avena en hojuelas integral', Alimento.GrupoAlimenticio.CARBOHIDRATOS, 50, Decimal('190.00'), Decimal('6.50'), Decimal('33.00'), Decimal('3.50')),
            ('Aguacate Hass fresco', Alimento.GrupoAlimenticio.GRASAS, 80, Decimal('128.00'), Decimal('1.60'), Decimal('6.80'), Decimal('11.70')),
            ('Brócoli al vapor', Alimento.GrupoAlimenticio.FRUTAS_VERDURAS, 150, Decimal('51.00'), Decimal('4.20'), Decimal('10.00'), Decimal('0.60')),
            ('Yogur griego natural sin azúcar', Alimento.GrupoAlimenticio.LACTEOS, 150, Decimal('90.00'), Decimal('15.00'), Decimal('5.50'), Decimal('0.80')),
            ('Salmón al horno', Alimento.GrupoAlimenticio.PROTEINAS, 120, Decimal('248.00'), Decimal('24.00'), Decimal('0.00'), Decimal('16.00')),
        ]
        alimentos = []
        for nom, grp, por, cal, prot, carb, gras in datos_alimentos:
            obj, _ = Alimento.objects.update_or_create(
                nombre=nom,
                defaults={
                    'grupo_alimenticio': grp,
                    'porcion_gramos': por,
                    'calorias': cal,
                    'proteinas_g': prot,
                    'carbohidratos_g': carb,
                    'grasas_g': gras,
                },
            )
            alimentos.append(obj)

        # 5 Pacientes (propiedad repartida entre carlos_consultor, ana_consultora y laura_admin)
        datos_pacientes = [
            ('1712345601', 'Andrea', 'Gómez Ruiz', date(1995, 4, 12), Paciente.Sexo.FEMENINO, '0981112201', 'andrea.gomez@correo.ec', 'Intolerancia leve a la lactosa.', user_consultor),
            ('1712345602', 'Diego', 'Almeida Soto', date(1988, 9, 23), Paciente.Sexo.MASCULINO, '0981112202', 'diego.almeida@correo.ec', 'Sin alergias conocidas. Deportista amateur.', user_consultor),
            ('1712345603', 'Sofía', 'Naranjo Vela', date(2001, 1, 15), Paciente.Sexo.FEMENINO, '0981112203', 'sofia.naranjo@correo.ec', 'Alergia a frutos secos (nueces).', user_consultora2),
            ('1712345604', 'Jorge', 'Castillo León', date(1979, 11, 30), Paciente.Sexo.MASCULINO, '0981112204', 'jorge.castillo@correo.ec', 'Hipertensión controlada, reducir sodio.', user_admin),
            ('1712345605', 'Elena', 'Cevallos Mora', date(1992, 6, 8), Paciente.Sexo.FEMENINO, '0981112205', 'elena.cevallos@correo.ec', 'Ninguna observación relevante.', user_admin),
        ]
        pacientes = []
        for ced, nom, ape, fnac, sex, tel, mail, aler, creador in datos_pacientes:
            obj, _ = Paciente.objects.update_or_create(
                cedula=ced,
                defaults={
                    'nombres': nom,
                    'apellidos': ape,
                    'fecha_nacimiento': fnac,
                    'sexo': sex,
                    'telefono': tel,
                    'email': mail,
                    'alergias_observaciones': aler,
                    'creado_por': creador,
                },
            )
            pacientes.append(obj)

        # 5 Planes Nutricionales con relación ManyToMany a Alimentos
        datos_planes = [
            ('Plan Déficit Calórico Moderado', PlanNutricional.ObjetivoPlan.PERDIDA_PESO, 1650, '5 comidas diarias, 2.5L de agua, priorizar proteína en cena.', date(2026, 11, 1), date(2026, 12, 15), user_consultor, [alimentos[0], alimentos[3], alimentos[4]]),
            ('Plan Hipertrofia y Rendimiento', PlanNutricional.ObjetivoPlan.GANANCIA_MUSCULAR, 2800, 'Carbohidratos complejos pre y post entrenamiento. Suplementación supervisada.', date(2026, 11, 5), date(2027, 1, 5), user_consultor, [alimentos[0], alimentos[1], alimentos[2], alimentos[5]]),
            ('Plan Hiposódico Cardiovascular', PlanNutricional.ObjetivoPlan.CLINICO, 1900, 'Eliminar embutidos y ultraprocesados. Usar especias naturales.', date(2026, 11, 10), date(2026, 12, 20), user_admin, [alimentos[3], alimentos[5], alimentos[2]]),
            ('Plan Equilibrio Metabólico', PlanNutricional.ObjetivoPlan.MANTENIMIENTO, 2100, 'Distribución 45% carbohidratos, 30% proteínas, 25% grasas saludables.', date(2026, 11, 12), date(2027, 1, 12), user_consultora2, [alimentos[1], alimentos[2], alimentos[4]]),
            ('Plan Recomposición Corporal', PlanNutricional.ObjetivoPlan.PERDIDA_PESO, 1850, 'Déficit ligero con alto aporte proteico para preservar masa magra.', date(2026, 11, 15), date(2026, 12, 30), user_admin, [alimentos[0], alimentos[4], alimentos[3]]),
        ]
        planes = []
        for nom, obj_plan, cal, ind, fini, ffin, creador, lista_alim in datos_planes:
            plan_obj, _ = PlanNutricional.objects.update_or_create(
                nombre=nom,
                defaults={
                    'objetivo': obj_plan,
                    'calorias_diarias': cal,
                    'indicaciones': ind,
                    'fecha_inicio': fini,
                    'fecha_fin': ffin,
                    'creado_por': creador,
                },
            )
            plan_obj.alimentos.set(lista_alim)
            planes.append(plan_obj)

        # 6 Consultas (propiedad repartida para probar edición/borrado propio vs ajeno)
        datos_consultas = [
            (pacientes[0], nutricionistas[0], planes[0], date(2026, 11, 10), Decimal('64.50'), 163, Decimal('35.00'), Consulta.EstadoConsulta.REALIZADA, 'Primera valoración nutricional. Inicia déficit moderado.', user_consultor),
            (pacientes[1], nutricionistas[1], planes[1], date(2026, 11, 12), Decimal('76.20'), 178, Decimal('40.00'), Consulta.EstadoConsulta.REALIZADA, 'Control deportivo mensual. Incremento de 1.1 kg de masa magra.', user_consultor),
            (pacientes[2], nutricionistas[2], planes[3], date(2026, 11, 15), Decimal('58.00'), 160, Decimal('35.00'), Consulta.EstadoConsulta.REALIZADA, 'Ajuste calórico de mantenimiento sin frutos secos.', user_consultora2),
            (pacientes[3], nutricionistas[0], planes[2], date(2026, 11, 18), Decimal('88.40'), 174, Decimal('45.00'), Consulta.EstadoConsulta.REALIZADA, 'Seguimiento clínico de presión arterial y perfil lipídico.', user_admin),
            (pacientes[4], nutricionistas[2], planes[4], date(2026, 11, 25), Decimal('69.00'), 166, Decimal('35.00'), Consulta.EstadoConsulta.PROGRAMADA, 'Consulta programada de seguimiento quincenal.', user_admin),
            (pacientes[0], nutricionistas[0], planes[0], date(2026, 11, 28), Decimal('63.20'), 163, Decimal('30.00'), Consulta.EstadoConsulta.PROGRAMADA, 'Control de evolución y ajuste de porciones.', user_consultor),
        ]
        for pac, nut, pln, fcon, peso, est, cost, est_c, diag, creador in datos_consultas:
            Consulta.objects.update_or_create(
                paciente=pac,
                fecha_consulta=fcon,
                defaults={
                    'nutricionista': nut,
                    'plan_nutricional': pln,
                    'peso_kg': peso,
                    'estatura_cm': est,
                    'costo': cost,
                    'estado': est_c,
                    'diagnostico_notas': diag,
                    'creado_por': creador,
                },
            )

        self.stdout.write(self.style.SUCCESS('3. Datos semilla cargados: 5 Nutricionistas, 6 Alimentos, 5 Pacientes, 5 Planes y 6 Consultas.'))