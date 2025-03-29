import React from "react";
import './ResultList.css'

interface ResultListProps {
    results: { [str: string]: string };
    searchTerm: string;
    loading: boolean;
    handleSelect: (key: string) => void;
    activeIndex: number;
}

export default function ResultList({
                                       results,
                                       searchTerm,
                                       loading,
                                       handleSelect,
                                       activeIndex,
                                   }: ResultListProps): React.JSX.Element {
    const matchedTerm = (name: string, searchTerm: string) => {
        const index = name.toLowerCase().indexOf(searchTerm.toLowerCase());
        if (index === -1) {
            return name;
        }
        return (
            <>
                {name.substring(0, index)}
                <b>{name.substring(index, index + searchTerm.length)}</b>
                {name.substring(index + searchTerm.length)}
            </>
        );
    };
    if (loading) {
        return <div className={"list"}>Loading...</div>;
    }

    if (Object.keys(results).length === 0) {
        return <div className={"list"}>No results found</div>;
    }
    return (
        <>
            <div className={"list"}>
                {Object.entries(results).map(([key, value], index) => (
                    <li key={key}
                        onClick={() => handleSelect(value)}
                        className={activeIndex === index ? "list-item active" : "list-item"}>
                        <>
                            {matchedTerm(value, searchTerm)}
                        </>
                    </li>
                ))}
            </div>
        </>
    );
}