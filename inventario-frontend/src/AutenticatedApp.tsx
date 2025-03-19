import logo from "./logo.svg";
import React, {useEffect, useState} from "react";
import {useAuth} from "react-oidc-context";
import {Button, Card, CardGroup, Container, Image, Stack} from "react-bootstrap";
import {Api, ListadoPaginadoAplicacionesDto, RequestParams} from "./openapi/api";

export function AutenticatedApp() {
    const auth = useAuth();
    const token = auth.user?.access_token;
    const rp = {headers: {Authorization: `Bearer ${token}`}} as RequestParams
    const api = new Api({
        baseUrl: `/api/v1`,
        baseApiParams: rp
    });
    function logOut() {
        auth.removeUser();
        auth.signoutRedirect();
    }

    const [aplicaciones, setAplicaciones] = useState({} as ListadoPaginadoAplicacionesDto);
    useEffect(() => {

        api.aplicaciones.getAplicaciones()
            .then(res => res.data)
            .then(data => {
                setAplicaciones(data);
            })
            .catch(err => console.error(err));
    }, []);

    return (
        <Container className="App-container">
            <p>Current time is {aplicaciones.total}</p>
            <Stack direction={"vertical"} gap={2}>
                <Card className="App-top p-0">
                    <Card.Body className="p-1">
                        <Image className="me-4" src={logo} alt="Logo Consejería" height={60}/>
                    </Card.Body>
                </Card>
                <Card className="App-content ">
                    <Card.Body>
                        <CardGroup>
                            <Card>
                                <Card.Body>Card1</Card.Body>
                            </Card>
                            <Card>
                                <Card.Body>Card1</Card.Body>
                            </Card>
                            <Card>
                                <Card.Body>Card2</Card.Body>
                            </Card>
                        </CardGroup>
                    </Card.Body>
                </Card>
                <Card className="App-bottom">
                    <Card.Body className="d-grid">
                        <Button variant={"danger"} onClick={() => logOut()}>Desconectar</Button>
                    </Card.Body>
                </Card>
            </Stack>
        </Container>

    );
}