import {Container} from "react-bootstrap";
import {Header} from "./Header";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Footer} from "./Footer";
import {Home} from "../pages/Home";
import {Sistemas} from "../pages/Sistemas";

export function Template() {
    return (
        <BrowserRouter>
            <Container className="Template-container p-0 ">
                <Header></Header>
                <div className="Template-content p-2 m-0">
                    <Routes>
                        <Route index element={<Home/>}/>
                        <Route path={"/home"} element={<Home/>}/>
                        <Route path={"/sistemas"} element={<Sistemas/>}/>
                    </Routes>
                </div>
                <Footer></Footer>
            </Container>
        </BrowserRouter>

    );
}