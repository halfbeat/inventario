import {Nav} from "react-bootstrap";

export function Footer() {

    return (
        <Nav activeKey="/home">
            <Nav.Item>
                <Nav.Link href={process.env.PUBLIC_URL + '/home'}>INVENTARIO DE APLICACIONES</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href={process.env.PUBLIC_URL + '/terminos-y-condiciones'}>Terminos y condiciones</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href={process.env.PUBLIC_URL + '/contacto'}>Contacto</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href={process.env.PUBLIC_URL + '/acercade'}> Acerca de </Nav.Link>
            </Nav.Item>
        </Nav>
    )
}