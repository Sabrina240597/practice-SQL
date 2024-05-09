import sqlite3
ruta = "C:/Users/sabri/AppData/Roaming/DBeaverData/workspace6/.metadata/sample-database-sqlite-1/Chinook.db"
conexion = sqlite3.connect(ruta)

cursor = conexion.cursor()
consulta = "SELECT * FROM Artist;"
cursor.execute(consulta)

#Obtener el listado de todos los productos ordenados por Nombre del Producto. 
#Mostrar: Nombre del Producto, Precio Unitario

cursor = conexion.cursor()
consulta = '''SELECT producto_nombre, precio_unitario;
FROM productos
ORDER BY producto_nombre'''
cursor.execute(consulta)

#btener el listado de la cantidad total de unidades para cada pedido
#Mostrar: Pedido, Cantidad
cursor = conexion.cursor()
consulta = '''SELECT pedido_ID, 
SUM (cantidad) AS cantidad_total 
FROM Pedidos_Detalle 
GROUP BY pedido_id'''
cursor.execute(consulta)

#Obtener el listado de todos los productos cuyo precio unitario se 
#encuentre entre 10 y 15 Mostrar: Nombre del Producto

cursor = conexion.cursor()
consulta = '''SELECT productos_nombre 
FROM productos 
WHERE Precio_unitario >=10 AND Precio_unitario <=15'''
cursor.execute(consulta)

#Obtener el mayor descuento realizado en algún pedido Mostrar: Descuento

cursor = conexion.cursor()
consulta = '''SELECT max (descuento) as max_descuento 
FROM pedidos_detalle'''
cursor.execute(consulta)

#Obtener el listado de todos los pedidos realizados en el año 
#1998 Mostrar: Todos los campos de Pedido

cursor = conexion.cursor()
consulta = '''SELECT * 
FROM pedidos 
WHERE extract (year from pedido_fecha) = '1998'''
cursor.execute(consulta)

#Obtener la cantidad de productos que tiene cada categoría. 
#Mostrar: Descripción de la Categoría, Cantidad de Productos

cursor = conexion.cursor()
consulta ='''SELECT c.categoria_descripcion, 
COUNT(Productos_nombre) AS cantidad_productos 
FROM categorias AS C 
INNER JOIN productos AS P ON = C.categoria_id = P.categoria_ID 
GROUP BY categoria_descripcion'''
cursor.execute(consulta)

#Obtener el listado de todos los empleados cuyo nombre comienzan con 'M'. 
#Mostrar: Nombre y Apellido del Empleado (En la misma columna)

cursor = conexion.cursor()
consulta ='''SELECT concat(empleado_nombre,' ', empleado_apellido) 
as empleado_nombre_completo 
FROM empleados 
WHERE empleado_nombre_completo LIKE 'M%';'''
cursor.execute(consulta)

#Obtener el nombre del producto cuyo precio unitario sea el mayor 
#Mostrar: Nombre del Producto, Precio Unitario

cursor = conexion.cursor()
consulta ='''SELECT producto_nombre, precio_unitario 
FROM producto 
WHERE precio_unitario = (select max(precio_unitario) from producto)'''
cursor.execute(consulta)

#Crear un Stored Procedure 'Actualiza_Precio’' que aumente en 
#un 10% el valor de los precios unitarios

cursor = conexion.cursor()
consulta ='''CREATE PROCEDURE Actualiza_Precio AS BEGIN UPDATE productos 
SET precio_unitario = (precio_unitario + precio_unitario*0.10) 
END GO;'''
cursor.execute(consulta)

#Crear un Stored Procedure 'Actualiza_Descuento’' para que reciba 
#por parámetro un valor de descuento a realizar y lo sume al ya existente, 
#sólo a los pedidos de los clientes de Alaska, Costa Dorada y California.

cursor = conexion.cursor()
consulta ='''CREATE PROCEDURE Actualiza_Descuento @descuento 
float AS BEGI N UPDATE pedidos_detalle
SET descuento = (descuento + @descuento) 
FROM pedidos_detalle pd 
INNER JOIN pedidos p ON pd.pedido_id = p.pedido_id 
INNER JOIN clientes c ON p.cliente_id = c.cliente_id 
WHERE c.cliente_pais = 'Alaska' OR c.cliente_ciudad in ('Costa Dorada', 'California') 
END GO;'''
cursor.execute(consulta)

#Listar la cantidad de unidades en stock para cada uno de los 
#productos que pertenecen a una categoría Mostrar: Descripción 
#de la categoría, Cantidad de unidades en stock

cursor = conexion.cursor()
consulta ='''SELECT c.categoria_descripcion ,
SUM(p.unidades_stock) AS cantidad_unidades_stock 
FROM producto p 
INNERJOIN categorias c ON p.categoria_id = c.categoria_id 
GROUP BY c.categoria_descripcion'''
cursor.execute(consulta)

#Listar todos los productos y la categoría a la que pertenecen. 
#Para las categorías desconocidas informar 'Sin Categoría' 
#Mostrar: Nombre del Producto, Nombre de la Categoría

cursor = conexion.cursor()
consulta ='''SELECT p.producto_nombre AS Nombre_Producto, 
ISNULL(c.categoria_nombre, 'Sin Categoría') AS Nombre_Categoría 
FROM producto p 
INNER JOIN categorias c ON p.categoria_id = c.categoria_id'''
cursor.execute(consulta)

#Listar las regiones que aún no cuenten con un proveedor 
#Mostrar : Nombre de la Región

cursor = conexion.cursor()
consulta ='''SELECT region_nombre FROM region AS R 
LEFT JOIN proveedor AS P ON R.region_id = P.prevedor_region 
WHERE p.prevedor_region IS NULL'''
cursor.execute(consulta)

#Listar los clientes que no entraron en mora 
#Mostrar: Nombre del cliente, Contacto del cliente

cursor = conexion.cursor()
consulta ='''SELECT c.cliente_nombre, c.cliente_contacto 
FROM clientes c 
LEFT JOIN clientes_morosos cm ON c.cliente_id = cm.cliente_id 
WHERE cm.cliente_id IS NULL'''
cursor.execute(consulta)

#Listar el monto total de mora de los clientes Antonio Moreno y 
#Maria Anders Mostrar: Monto total de mora (De ambos clilentes)

cursor = conexion.cursor()
consulta ='''SELECT c.cliente_id, 
SUM(cm.mora) mora 
FROM clientes AS c 
INNER JOIN clientes_morosos cm ON c.cliente_id = cm.cliente_id 
WHERE c.cliente_nombre in ('Antonio Moreno', 'Maria Anders')'''
cursor.execute(consulta)

#Listar el monto total de descuento aplicado a los clientes no morosos. 
#Agrupar el listado por cada una de las categorías conocidas y no conocidas. 
#En el último caso informar Sin Categoría. Mostrar: Nombre de la Categoría, Descuento.

cursor = conexion.cursor()
consulta ='''SUM(pedidos_detalle.descuento) AS descuento 
FROM clientes 
LEFT JOIN clientes_morosos ON clientes.cliente_id = clientes_morosos.cliente_id 
INNER JOIN pedidos ON pedidos.cliente_id = clientes.cliente_id 
INNER JOIN pedidos_detalle ON pedidos.pedido_id = pedidos_detalle.pedido_id 
INNER JOIN productos ON pedidos_detalle.producto_id = productos.producto_id 
INNER JOIN categorias ON categorias.categoria_id = productos.categoria_id 
WHERE clientes_morosos.cliente_id IS NULL 
GROUP BY categorias.categoria_nombre'''
cursor.execute(consulta)

#Listar a todos los empleados y a su jefe (Según a quién reporta el empleado) 
#Mostrar : Nombre del Empleado, Nombre del Jefe

cursor = conexion.cursor()
consulta ='''SELECT concat(e.empleado_nombre, ' ', e.empleado_apellido) AS nombre_empleado, 
empleado_reporta_a AS nombre_jefe 
FROM empleados'''
cursor.execute(consulta)

#insertar datos de tabla y cambiar tipos los tipos de datos 
#de VENTAS_POR_FACTURA a la tabla TABLA_NUEVA

cursor = conexion.cursor()
consulta ='''INSERT INTO tabla_nueva (numero_factura, fecha_factura, id_cliente, Pais, Cantidad, Monto) 
SELECT n_de_factura, CONVERT(datetime2(7), fecha_de_factura), 
CAST(coalesce(id_cliente, '0') as int), País, 
CAST(Cantidad AS INT), 
cast(replace(monto, ',', '.') as decimal)
FROM ventas_por_factura;

select * from tabla_nueva'''
cursor.execute(consulta)

resultados = cursor.fetchall()
for fila in resultados:
    print(fila)

cursor.close()
conexion.close()
