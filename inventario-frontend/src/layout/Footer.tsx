import {Nav} from "react-bootstrap";

export function Footer() {

    return (
        <Nav activeKey="/home">
            <Nav.Item>
                <Nav.Link href="/home">INVENTARIO DE APLICACIONES</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href="/terminos-y-condiciones">Terminos y condiciones</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href="/contacto">Contacto</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href="/acercade"> Acerca de </Nav.Link>
            </Nav.Item>
        </Nav>
    )
}