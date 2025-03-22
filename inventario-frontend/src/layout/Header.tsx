import {Button, Col, Image, Row, Stack} from "react-bootstrap";
import logoConsejeria from "../assets/logo_consejeria.png";
import logoGSS from "../assets/logo_gss.png";
import React from "react";
import './Template.scss';
import {useAuth} from "react-oidc-context";
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
        <Row className={"pt-2 align-items-center border-bottom"}>
            <Col>
                <h3>INVENTARIO DE SISTEMAS</h3>
            </Col>
            <Col md={4}>
                <Stack direction={"horizontal"} className={"float-end"} gap={1}>
                    <Image className="img-fluid" src={logoConsejeria} alt="Logo Consejería" width={"40%"}/>
                    <Image className="img-fluid" src={logoGSS} alt="Logo GSS" width={"40%"}/>
                </Stack>
            </Col>
            <Col md={2} className={"text-center"}>
                <Stack direction={"vertical"} gap={1}>
                    <FontAwesomeIcon className={user == null ? 'opacity-25' : ''} size={"3x"}
                                     icon={["fas", "user-circle"]}/>
                    <Button hidden={user == null} variant={"link"} onClick={() => logOut()}>Desconectar</Button>
                    <Button hidden={user != null} variant={"link"} onClick={() => void auth.signinRedirect()}>Iniciar
                        sesión</Button>
                </Stack>
            </Col>

        </Row>
    )
}