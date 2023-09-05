<h1 align="center">practicando SQL!</h1>
<h3 align="center">challenge de practica</h3>

<p align="left"> <img src="https://komarev.com/ghpvc/?username=sabrina240597&label=Profile%20views&color=0e75b6&style=flat" alt="sabrina240597" /> </p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://www.microsoft.com/en-us/sql-server" target="_blank" rel="noreferrer"> <img src="https://www.svgrepo.com/show/303229/microsoft-sql-server-logo.svg" alt="mssql" width="40" height="40"/> </a> <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a> </p>


1) Obtener el listado de todos los productos ordenados por Nombre del Producto.
   Mostrar: Nombre del Producto, Precio Unitario

SELECT producto_nombre, precio_unitario
FROM productos
ORDER BY producto_nombre


2) Obtener el listado de la cantidad total de unidades para cada pedido  
   Mostrar: Pedido, Cantidad

SELECT pedido_ID, 
SUM (cantidad) AS cantidad_total
FROM Pedidos_Detalle
GROUP BY pedido_id


3) Obtener el listado de todos los productos cuyo precio unitario se encuentre entre 10 y 15
   Mostrar: Nombre del Producto

 SELECT productos_nombre
 FROM productos
 WHERE Precio_unitario >=10 AND Precio_unitario <=15


4) Obtener el mayor descuento realizado en algún pedido
   Mostrar: Descuento

SELECT max (descuento) as max_descuento
FROM pedidos_detalle


5) Obtener el listado de todos los pedidos realizados en el año 1998
   Mostrar: Todos los campos de Pedido
   
SELECT *
FROM pedidos
WHERE  extract (year from pedido_fecha) = '1998'


6) Obtener la cantidad de productos que tiene cada categoría. 
  Mostrar: Descripción de la Categoría, Cantidad de Productos

SELECT c.categoria_descripcion, COUNT(Productos_nombre) AS cantidad_productos
FROM categorias AS C
INNER JOIN productos AS P 
ON = C.categoria_id = P.categoria_ID
GROUP BY categoria_descripcion


7) Obtener el listado  de todos los empleados cuyo nombre comienzan con 'M'.
   Mostrar: Nombre y Apellido del Empleado (En la misma columna)

SELECT concat(empleado_nombre,' ', empleado_apellido) as empleado_nombre_completo
FROM empleados
WHERE empleado_nombre_completo LIKE 'M%';


8) Obtener el nombre del producto cuyo precio unitario sea el mayor
   Mostrar: Nombre del Producto, Precio Unitario

SELECT  producto_nombre, precio_unitario
FROM producto
WHERE precio_unitario = (select max(precio_unitario) from producto)


9)  Crear un Stored Procedure 'Actualiza_Precio’' que aumente en un 10% el valor de los precios unitarios

CREATE PROCEDURE Actualiza_Precio
AS 
BEGIN
UPDATE productos SET precio_unitario = (precio_unitario + precio_unitario*0.10)
END
GO;


10) Crear un Stored Procedure 'Actualiza_Descuento’' para que reciba por parámetro un valor de descuento a realizar y lo sume al ya existente, sólo a los pedidos de los clientes de Alaska, Costa Dorada y California.

CREATE PROCEDURE Actualiza_Descuento @descuento float
AS 
BEGI N 
UPDATE pedidos_detalle
SET descuento = (descuento + @descuento)
FROM pedidos_detalle pd
I NNER JOIN pedidos p
ON pd.pedido_id = p.pedido_id
I NNER JOIN clientes c
ON p.cliente_id = c.cliente_id
WHERE c.cliente_pais = 'Alaska'
OR c.cliente_ciudad in ('Costa Dorada', 'California') 
END
GO;


11) Listar la cantidad de unidades en stock para cada uno de los productos que pertenecen a una categoría
    Mostrar:  Descripción de la categoría, Cantidad de unidades en stock

SELECT c.categoria_descripcion ,SUM(p.unidades_stock) AS cantidad_unidades_stock
FROM producto p
I NNERJOIN categorias c
ON p.categoria_id = c.categoria_id
GROUP BY c.categoria_descripcion


12) Listar todos los productos y la categoría a la que pertenecen. Para las categorías desconocidas informar 'Sin Categoría'
    Mostrar: Nombre del Producto, Nombre de la Categoría  

SELECT  p.producto_nombre AS Nombre_Producto,
ISNULL(c.categoria_nombre, 'Sin Categoría') AS Nombre_Categoría
FROM producto p
I NNER JOIN categorias c
ON p.categoria_id = c.categoria_id


13) Listar las regiones que aún no cuenten con un proveedor
    Mostrar : Nombre de la Región

SELECT  region_nombre
FROM  region AS R
LEFT JOIN  proveedor AS P
ON R.region_id = P.prevedor_region
WHERE  p.prevedor_region IS NULL


14) Listar los clientes que no entraron en mora
    Mostrar: Nombre del cliente, Contacto del cliente

SELECT c.cliente_nombre, c.cliente_contacto
FROM  clientes c
LEFT JOIN clientes_morosos cm
ON c.cliente_id = cm.cliente_id
WHERE cm.cliente_id IS NULL


15) Listar el monto total de mora de los clientes Antonio Moreno y Maria Anders
    Mostrar: Monto total de mora (De ambos clilentes)

SELECT c.cliente_id, SUM(cm.mora) mora
FROM clientes AS c
INNER JOIN clientes_morosos cm
ON c.cliente_id = cm.cliente_id
WHERE c.cliente_nombre in ('Antonio Moreno', 'Maria Anders')

 
16) Listar el monto total de descuento aplicado a los clientes no morosos. Agrupar el listado por cada una de las categorías conocidas y no conocidas. En el último caso informar Sin Categoría.
Mostrar: Nombre de la Categoría, Descuento.

SELECT ISNULL(categorias.categoria_nombre, 'Sin Categoría') AS Nombre_Categoría, SUM(pedidos_detalle.descuento) AS descuento
FROM clientes
LEFT JOIN clientes_morosos
ON clientes.cliente_id = clientes_morosos.cliente_id
INNER JOIN pedidos
ON pedidos.cliente_id = clientes.cliente_id
INNER JOIN pedidos_detalle
ON pedidos.pedido_id = pedidos_detalle.pedido_id
INNER JOIN productos
ON pedidos_detalle.producto_id = productos.producto_id
INNER JOIN categorias
ON categorias.categoria_id = productos.categoria_id
WHERE clientes_morosos.cliente_id IS NULL
GROUP BY categorias.categoria_nombre


17)  Listar a todos los empleados y a su jefe (Según a quién reporta el empleado)
    Mostrar : Nombre del Empleado, Nombre del Jefe

SELECT concat(e.empleado_nombre, ' ', e.empleado_apellido) AS nombre_empleado, empleado_reporta_a AS nombre_jefe
FROM empleados


18) insertar datos de tabla y cambiar tipos los tipos de datos de VENTAS_POR_FACTURA a la tabla TABLA_NUEVA

INSERT INTO tabla_nueva
(numero_factura, fecha_factura, id_cliente, Pais, Cantidad, Monto)
SELECT 
    n_de_factura, 
    CONVERT(datetime2(7), fecha_de_factura), 
    CAST(coalesce(id_cliente, '0') as int), 
    País,
    CAST(Cantidad AS INT), 
    cast(replace(monto, ',', '.') as decimal)
FROM ventas_por_factura;

select *
from tabla_nueva

