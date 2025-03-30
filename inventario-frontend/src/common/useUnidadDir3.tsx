import React, {useEffect} from "react";
import {UnidadDIR3Dto} from "../openapi/api";
import useApi from "./useApi";

export default function useUnidadDir3(codigo_unidad: string | undefined) {
    const [unidad, setUnidad] = React.useState<UnidadDIR3Dto | undefined>();
    const [loading, setLoading] = React.useState(false);

    const api = useApi();

    useEffect(() => {
        setLoading(true);
        if (!codigo_unidad) {
            setLoading(false);
            return setUnidad(unidad);
        }

        let key = "unidaddir3_" + codigo_unidad;
        const cachedData = sessionStorage.getItem(key);
        if (cachedData) {
            setUnidad(JSON.parse(cachedData));
            setLoading(false);
            return;
        }
        const getUnidadDir3 = setTimeout(async () => {
            try {
                api?.dir3.getUnidadDir3(codigo_unidad)
                    .then(res => res.data)
                    .then(data => {
                        setUnidad(data);
                        setLoading(false);
                        sessionStorage.setItem(key, JSON.stringify(data));
                    })
                    .catch(err => console.log(err));

            } catch (error) {
                console.error(error);
            }
        }, 300);
        return () => clearTimeout(getUnidadDir3);
    }, [codigo_unidad]);

    return {unidadDir3: unidad, loadingUnidad: loading};
}