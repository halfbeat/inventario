import {Button, Container, Image, Stack} from "react-bootstrap";
import React from "react";
import {useAuth} from "react-oidc-context";
import './AnonymousApp.scss';
import logoConsejeria from './logo_consejeria.png'
import logoGSS from './logo_gss.png'

export function AnonymousApp() {
    const auth = useAuth();


    return (
        <Container className="App-container">

            <Stack direction={"vertical"} gap={2}>
                <div className="App-top">
                    <Stack direction={"horizontal"} gap={2}>
                        {/*<Image className="me-4" src={logo} alt="Logo Consejería" height={60}/>*/}
                        <h1 className={"mx-auto"}>Familias CyL</h1>
                    </Stack>
                </div>
                <div className="App-content sticky-top">
                    <Stack direction={"vertical"} gap={2}>
                        <Stack direction={"horizontal"} gap={4} className={"border-bottom pb-2"}>
                            <Image className="mx-auto" src={logoConsejeria} alt="Logo Consejería"  width={"50%"}/>
                            <Image className="mx-auto" src={logoGSS} alt="Logo GSS" width={"50%"}/>
                        </Stack>
                        <h1>FAMILIAS</h1>
                        <p>Este es el contenido</p>
                    </Stack>
                </div>
                <div className="App-bottom d-grid">
                    <Button variant={"danger"} onClick={() => void auth.signinRedirect()}>Acceder</Button>
                </div>
            </Stack>
        </Container>
    )
}