import {Container, Nav, Navbar, Stack} from "react-bootstrap";
import React from "react";
import './Template.scss';
import {useAuth} from "react-oidc-context";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export function Header() {
    const auth = useAuth();
    const user = auth.user;

    function logOut() {
        auth.removeUser()
            .then(() => auth.signoutRedirect({
                id_token_hint: user?.id_token,
            }).then(() => auth.clearStaleState()))
            .catch((error) => alert(JSON.stringify(error)));

    }

    return (
        <Navbar variant="light" expand="lg" className={"bg-body-secondary justify-content-between"}>
            <Container>
                <Navbar.Brand as={Link} to="/home">INVENTARIO DE SISTEMAS</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/home">Inicio </Nav.Link>
                        <Nav.Link as={Link} to="/sistemas">Sistemas</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
            <Stack direction={"horizontal"} gap={2} className="me-1">
                <FontAwesomeIcon className={user == null ? 'opacity-25' : ''} size={"2x"}
                                 icon={["fas", "user-circle"]}/>
                {(auth.user?.profile as any)?.principal}

                <Nav.Link className="p-0 m-0" hidden={user == null} onClick={() => logOut()}>Desconectar</Nav.Link>
                <Nav.Link className="p-0 m-0" hidden={user != null} onClick={() => void auth.signinRedirect()}>Iniciar
                    sesión</Nav.Link>
            </Stack>
        </Navbar>
        // <Row className={"pt-2 align-items-center border-bottom"}>
        //     <Col>
        //         <h3>INVENTARIO DE SISTEMAS</h3>
        //     </Col>
        //     <Col md={4}>
        //         <Stack direction={"horizontal"} className={"float-end"} gap={1}>
        //             <Image className="img-fluid" src={logoConsejeria} alt="Logo Consejería" width={"40%"}/>
        //             <Image className="img-fluid" src={logoGSS} alt="Logo GSS" width={"40%"}/>
        //         </Stack>
        //     </Col>
        //     <Col md={2} className={"text-center"}>
        //         <Stack direction={"vertical"} gap={1}>
        //             <FontAwesomeIcon className={user == null ? 'opacity-25' : ''} size={"3x"}
        //                              icon={["fas", "user-circle"]}/>
        //             {(auth.user?.profile as any)?.principal}
        //             <Button hidden={user == null} variant={"link"} onClick={() => logOut()}>Desconectar</Button>
        //             <Button hidden={user != null} variant={"link"} onClick={() => void auth.signinRedirect()}>Iniciar
        //                 sesión</Button>
        //         </Stack>
        //     </Col>
        //
        // </Row>
    )
}