import React, {useEffect} from "react";
import {UnidadDIR3Dto} from "../openapi/api";
import useApi from "./useApi";

export type QueryDir3Fields = {
    id: string
    nombre: string
}

export default function useUnidadesDir3(searchTerm: string) {
    const [unidades, setUnidades] = React.useState<UnidadDIR3Dto[]>([]);
    const [loading, setLoading] = React.useState(false);

    const api = useApi();

    useEffect(() => {
        setLoading(true);
        if (!searchTerm) {
            setLoading(false);
            return setUnidades([]);
        }

        let key = "unidadesdir3_" + searchTerm;
        const cachedData = sessionStorage.getItem(key);
        if (cachedData) {
            setUnidades(JSON.parse(cachedData));
            setLoading(false);
            return;
        }
        const getUnidadesDir3 = setTimeout(async () => {
            try {
                api?.dir3.queryUnidadesDir3({nombre: searchTerm})
                    .then(res => res.data)
                    .then(data => {
                        setUnidades(data.items);
                        setLoading(false);
                        sessionStorage.setItem(key, JSON.stringify(data.items));
                    })
                    .catch(err => console.log(err));

            } catch (error) {
                console.error(error);
            }
        }, 300);
        return () => clearTimeout(getUnidadesDir3);
    }, [searchTerm]);

    return {unidadesDir3: unidades, loading};
}