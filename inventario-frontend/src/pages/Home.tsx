import {Configuration} from '../Configuration'

export function Home() {
    const val = Configuration.prop1;
    return (
        <p>Hogar dulce hogar: {val} y {process.env.NODE_ENV}</p>
    )
}