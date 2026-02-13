"""
GUI Web del sistema GIC usando Flask.
Reemplaza Tkinter por una interfaz web accesible desde el navegador.
"""
from flask import Flask, render_template_string, request, redirect, url_for, flash
from src.services.cliente_service import ClienteService
from src.database.migrations import crear_tablas
from src.exceptions.validation_errors import GICValidationError
from src.exceptions.database_errors import RegistroDuplicadoError

app = Flask(__name__)
app.secret_key = "gic-secret-key"
service = ClienteService()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GIC - Gestor Inteligente de Clientes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #F3F4F6; color: #1F2937; }
        .header { background: #2563EB; color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { font-size: 20px; }
        .header .stats { font-size: 13px; opacity: 0.9; }
        .toolbar { background: white; padding: 12px 24px; border-bottom: 1px solid #E5E7EB; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
        .btn { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; text-decoration: none; display: inline-block; }
        .btn-primary { background: #10B981; color: white; }
        .btn-primary:hover { background: #059669; }
        .btn-danger { background: #EF4444; color: white; }
        .btn-danger:hover { background: #DC2626; }
        .btn-secondary { background: #6B7280; color: white; }
        .btn-secondary:hover { background: #4B5563; }
        .btn-outline { background: white; color: #374151; border: 1px solid #D1D5DB; }
        .btn-outline:hover { background: #F9FAFB; }
        .search-box { padding: 8px 12px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 13px; width: 200px; }
        select { padding: 8px 12px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 13px; }
        .container { padding: 24px; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th { background: #F9FAFB; padding: 12px 16px; text-align: left; font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; border-bottom: 1px solid #E5E7EB; }
        td { padding: 12px 16px; border-bottom: 1px solid #F3F4F6; font-size: 14px; }
        tr:hover { background: #F9FAFB; }
        .badge { padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .badge-regular { background: #DBEAFE; color: #1D4ED8; }
        .badge-premium { background: #EDE9FE; color: #7C3AED; }
        .badge-corporativo { background: #D1FAE5; color: #065F46; }
        .badge-activo { background: #D1FAE5; color: #065F46; }
        .badge-inactivo { background: #FEE2E2; color: #991B1B; }
        .actions a { margin-right: 8px; font-size: 13px; }
        .flash { padding: 12px 24px; margin: 0; font-size: 14px; }
        .flash-success { background: #D1FAE5; color: #065F46; }
        .flash-error { background: #FEE2E2; color: #991B1B; }
        .form-container { max-width: 600px; margin: 0 auto; background: white; padding: 32px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; margin-bottom: 4px; font-size: 13px; font-weight: 500; color: #374151; }
        .form-group input, .form-group select { width: 100%; padding: 10px 12px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 14px; }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
        .extra-fields { background: #F9FAFB; padding: 16px; border-radius: 6px; margin-top: 16px; }
        .extra-fields h3 { font-size: 14px; margin-bottom: 12px; color: #4B5563; }
        .form-actions { margin-top: 24px; display: flex; gap: 8px; }
        .separator { width: 1px; height: 24px; background: #D1D5DB; margin: 0 8px; }
        .empty-state { text-align: center; padding: 60px; color: #9CA3AF; }
        .empty-state p { font-size: 16px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>GIC - Gestor Inteligente de Clientes</h1>
        <div class="stats">{{ stats_text }}</div>
    </div>
    {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
    <div class="flash flash-{{ category }}">{{ message }}</div>
    {% endfor %}
    {% endwith %}
    {% block content %}{% endblock %}
</body>
</html>
"""

LIST_PAGE = """
{% extends "base" %}
{% block content %}
<div class="toolbar">
    <a href="/nuevo" class="btn btn-primary">+ Nuevo Cliente</a>
    <div class="separator"></div>
    <a href="/exportar/json" class="btn btn-outline">Exportar JSON</a>
    <a href="/exportar/csv" class="btn btn-outline">Exportar CSV</a>
    <div class="separator"></div>
    <form method="GET" action="/" style="display:flex; gap:8px; align-items:center;">
        <input type="text" name="busqueda" placeholder="Buscar..." class="search-box" value="{{ busqueda or '' }}">
        <select name="tipo" onchange="this.form.submit()">
            <option value="">Todos los tipos</option>
            <option value="Regular" {{ 'selected' if tipo == 'Regular' }}>Regular</option>
            <option value="Premium" {{ 'selected' if tipo == 'Premium' }}>Premium</option>
            <option value="Corporativo" {{ 'selected' if tipo == 'Corporativo' }}>Corporativo</option>
        </select>
        <button type="submit" class="btn btn-outline">Buscar</button>
    </form>
</div>
<div class="container">
{% if clientes %}
<table>
    <thead>
        <tr>
            <th>Nombre</th><th>Email</th><th>Telefono</th><th>Tipo</th><th>Estado</th><th>Direccion</th><th>Acciones</th>
        </tr>
    </thead>
    <tbody>
    {% for c in clientes %}
        <tr>
            <td><strong>{{ c.nombre }}</strong></td>
            <td>{{ c.email }}</td>
            <td>{{ c.telefono }}</td>
            <td><span class="badge badge-{{ c.tipo_cliente|lower }}">{{ c.tipo_cliente }}</span></td>
            <td><span class="badge badge-{{ 'activo' if c.activo else 'inactivo' }}">{{ 'Activo' if c.activo else 'Inactivo' }}</span></td>
            <td>{{ c.direccion }}</td>
            <td class="actions">
                <a href="/editar/{{ c.id }}">Editar</a>
                <a href="/toggle/{{ c.id }}">{{ 'Desactivar' if c.activo else 'Activar' }}</a>
                <a href="/eliminar/{{ c.id }}" style="color:#EF4444;" onclick="return confirm('Eliminar a {{ c.nombre }}?')">Eliminar</a>
            </td>
        </tr>
    {% endfor %}
    </tbody>
</table>
{% else %}
<div class="empty-state"><p>No hay clientes registrados. Crea el primero!</p></div>
{% endif %}
</div>
{% endblock %}
"""

FORM_PAGE = """
{% extends "base" %}
{% block content %}
<div class="container">
<div class="form-container">
    <h2 style="margin-bottom:24px;">{{ 'Editar Cliente' if editando else 'Nuevo Cliente' }}</h2>
    <form method="POST">
        <div class="form-group">
            <label>Tipo de Cliente</label>
            <select name="tipo" id="tipo" onchange="toggleExtra()" {{ 'disabled' if editando }}>
                <option value="Regular" {{ 'selected' if tipo == 'Regular' }}>Regular</option>
                <option value="Premium" {{ 'selected' if tipo == 'Premium' }}>Premium</option>
                <option value="Corporativo" {{ 'selected' if tipo == 'Corporativo' }}>Corporativo</option>
            </select>
            {% if editando %}<input type="hidden" name="tipo" value="{{ tipo }}">{% endif %}
        </div>
        <div class="form-group"><label>Nombre</label><input type="text" name="nombre" value="{{ nombre or '' }}" required></div>
        <div class="form-group"><label>Email</label><input type="email" name="email" value="{{ email or '' }}" required></div>
        <div class="form-group"><label>Telefono (ej: +56944556677)</label><input type="text" name="telefono" value="{{ telefono or '' }}" required></div>
        <div class="form-group"><label>Direccion</label><input type="text" name="direccion" value="{{ direccion or '' }}" required></div>
        <div id="premium-fields" class="extra-fields" style="display:none;">
            <h3>Datos Premium</h3>
            <div class="form-group"><label>Nivel</label>
                <select name="nivel_premium">
                    <option value="Gold" {{ 'selected' if nivel_premium == 'Gold' }}>Gold</option>
                    <option value="Platinum" {{ 'selected' if nivel_premium == 'Platinum' }}>Platinum</option>
                    <option value="Diamond" {{ 'selected' if nivel_premium == 'Diamond' }}>Diamond</option>
                </select>
            </div>
            <div class="form-group"><label>Asesor Dedicado</label><input type="text" name="asesor_dedicado" value="{{ asesor_dedicado or '' }}"></div>
        </div>
        <div id="corp-fields" class="extra-fields" style="display:none;">
            <h3>Datos Corporativos</h3>
            <div class="form-group"><label>RUT Empresa</label><input type="text" name="rut_empresa" value="{{ rut_empresa or '' }}"></div>
            <div class="form-group"><label>Razon Social</label><input type="text" name="razon_social" value="{{ razon_social or '' }}"></div>
            <div class="form-group"><label>Rubro</label><input type="text" name="rubro" value="{{ rubro or '' }}"></div>
            <div class="form-group"><label>Contacto Comercial</label><input type="text" name="contacto_comercial" value="{{ contacto_comercial or '' }}"></div>
            <div class="form-group"><label>Cantidad Empleados</label><input type="number" name="cantidad_empleados" value="{{ cantidad_empleados or 1 }}" min="1"></div>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">{{ 'Actualizar' if editando else 'Crear Cliente' }}</button>
            <a href="/" class="btn btn-outline">Cancelar</a>
        </div>
    </form>
</div>
</div>
<script>
function toggleExtra() {
    var tipo = document.getElementById('tipo').value;
    document.getElementById('premium-fields').style.display = tipo === 'Premium' ? 'block' : 'none';
    document.getElementById('corp-fields').style.display = tipo === 'Corporativo' ? 'block' : 'none';
}
toggleExtra();
</script>
{% endblock %}
"""


def get_stats_text():
    stats = service.estadisticas()
    return f"Total: {stats['total']} | Regular: {stats['regulares']} | Premium: {stats['premium']} | Corp: {stats['corporativos']}"


@app.route("/")
def index():
    tipo = request.args.get("tipo")
    busqueda = request.args.get("busqueda")
    clientes = service.listar_clientes(tipo=tipo, busqueda=busqueda)
    clientes_data = [c.to_dict() for c in clientes]
    template = HTML_TEMPLATE.replace("{% block content %}{% endblock %}", LIST_PAGE.replace('{% extends "base" %}\n{% block content %}', '').replace('{% endblock %}', ''))
    return render_template_string(template, clientes=clientes_data, stats_text=get_stats_text(), tipo=tipo, busqueda=busqueda)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        tipo = request.form.get("tipo", "Regular")
        datos = {
            "nombre": request.form["nombre"],
            "email": request.form["email"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
        }
        if tipo == "Premium":
            datos["nivel_premium"] = request.form.get("nivel_premium", "Gold")
            datos["asesor_dedicado"] = request.form.get("asesor_dedicado", "Sin asignar")
        elif tipo == "Corporativo":
            datos["rut_empresa"] = request.form.get("rut_empresa", "")
            datos["razon_social"] = request.form.get("razon_social", "")
            datos["rubro"] = request.form.get("rubro", "No especificado")
            datos["contacto_comercial"] = request.form.get("contacto_comercial", "")
            datos["cantidad_empleados"] = int(request.form.get("cantidad_empleados", 1))
        try:
            cliente = service.crear_cliente(tipo, **datos)
            flash(f"Cliente '{cliente.nombre}' creado exitosamente", "success")
            return redirect("/")
        except (GICValidationError, RegistroDuplicadoError, ValueError) as e:
            flash(str(e), "error")
            template = HTML_TEMPLATE.replace("{% block content %}{% endblock %}", FORM_PAGE.replace('{% extends "base" %}\n{% block content %}', '').replace('{% endblock %}', ''))
            return render_template_string(template, stats_text=get_stats_text(), editando=False, **request.form)
    template = HTML_TEMPLATE.replace("{% block content %}{% endblock %}", FORM_PAGE.replace('{% extends "base" %}\n{% block content %}', '').replace('{% endblock %}', ''))
    return render_template_string(template, stats_text=get_stats_text(), editando=False, tipo="Regular", nombre="", email="", telefono="", direccion="", nivel_premium="Gold", asesor_dedicado="", rut_empresa="", razon_social="", rubro="", contacto_comercial="", cantidad_empleados=1)


@app.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    try:
        cliente = service.obtener_cliente(id)
    except Exception:
        flash("Cliente no encontrado", "error")
        return redirect("/")
    if request.method == "POST":
        datos = {
            "nombre": request.form["nombre"],
            "email": request.form["email"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
        }
        try:
            service.actualizar_cliente(id, **datos)
            flash("Cliente actualizado", "success")
            return redirect("/")
        except (GICValidationError, ValueError) as e:
            flash(str(e), "error")
    d = cliente.to_dict()
    template = HTML_TEMPLATE.replace("{% block content %}{% endblock %}", FORM_PAGE.replace('{% extends "base" %}\n{% block content %}', '').replace('{% endblock %}', ''))
    return render_template_string(template, stats_text=get_stats_text(), editando=True, tipo=d.get("tipo_cliente","Regular"), nombre=d["nombre"], email=d["email"], telefono=d["telefono"], direccion=d["direccion"], nivel_premium=d.get("nivel_premium","Gold"), asesor_dedicado=d.get("asesor_dedicado",""), rut_empresa=d.get("rut_empresa",""), razon_social=d.get("razon_social",""), rubro=d.get("rubro",""), contacto_comercial=d.get("contacto_comercial",""), cantidad_empleados=d.get("cantidad_empleados",1))


@app.route("/eliminar/<id>")
def eliminar(id):
    try:
        service.eliminar_cliente(id)
        flash("Cliente eliminado", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect("/")


@app.route("/toggle/<id>")
def toggle(id):
    try:
        cliente = service.obtener_cliente(id)
        if cliente.activo:
            service.desactivar_cliente(id)
            flash("Cliente desactivado", "success")
        else:
            cliente.activar()
            from src.repositories.sqlite_repository import SQLiteRepository
            SQLiteRepository().actualizar(cliente)
            flash("Cliente activado", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect("/")


@app.route("/exportar/json")
def exportar_json():
    ruta = service.exportar_json()
    flash(f"Exportado a JSON: {ruta}", "success")
    return redirect("/")


@app.route("/exportar/csv")
def exportar_csv():
    ruta = service.exportar_csv()
    flash(f"Exportado a CSV: {ruta}", "success")
    return redirect("/")


def iniciar_gui():
    crear_tablas()
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == "__main__":
    iniciar_gui()
