import {Container} from "react-bootstrap";
import {Header} from "./Header";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Footer} from "./Footer";
import {Home} from "../pages/Home";

export function Template() {
    return (
        <Container className="Template-container">
            <Header></Header>
            <div className="Template-content" >
                <BrowserRouter>
                    <Routes>
                        <Route index element={<Home/>}/>
                        <Route path={"/home"} element={<Home/>}/>
                    </Routes>
                    <p>ME ves siempre</p>
                </BrowserRouter>
            </div>
            <Footer></Footer>
        </Container>

    );
}