import { Dispatch, SetStateAction, useEffect, useState } from "react"
import { User as UserType } from "../Interfaces.tsx"
import { capitalizeFirstLetter as cfl } from "../helpers/text_formaters.tsx"


interface JobProps {
    setScrapePage: Dispatch<React.SetStateAction<boolean>>
    userJobs: UserType | null
    setUserJobs: Dispatch<SetStateAction<UserType | null>>;
}

export default function ScrapeJobs({ userJobs, setUserJobs, setScrapePage }: JobProps) {
    const [job, setJob] = useState<string>("")
    const [location, setLocation] = useState<string>("")
    const [scriptExecution, setScriptExecution] = useState<boolean>(false)
    const url = window.location.href;

    const pathParts = url.split('/');
    const userId = pathParts[pathParts.length - 1]; // Gets the last part of the URL

    const fetchUserJobs = async (userId: string) => {
        const response = await fetch(`http://127.0.0.1:5000/jobs/user/${userId}`);
        const userJobsData = await response.json();
        console.log(userJobsData)
        setUserJobs(userJobsData);
    };
    //󰙧

    const activateScraping = async (job: string, location: string) => {
        console.log("Parameters to send:", job, location);
        setScriptExecution(true)
        try {
            const response = await fetch(`http://127.0.0.1:5000/runscript/${job}/${location}`, { method: 'POST' });
            const data = await response.json();
            console.log('Response from server:', data);
            setScriptExecution(false)
        } catch (error) {
            console.error('Error during fetch:', error);
        }
    };

    const play = () => {
        let wscreen = window.screen.width
        let time = time
        console.log(wscreen)
    }

    useEffect(() => {
        fetchUserJobs(userId)
    }, [])


    return (
        <>
            <div className="flex h-24 px-20 bg-amber-800 justify-center gap-5">
                <div className="w-1/3 h-4/6 self-center gap-3 flex">
                    <div className="self-center">
                        <p className="font-bold text-white">Job</p>
                        <input className="bg-grey-50 w-full py-2 font-medium px-3 leading-tight focus:outline-none focus:shadow-outline"
                            onChange={(e) => setJob(e.target.value)}
                            value={job}
                        />
                    </div>
                </div>
                <div className="w-1/3 h-4/6 self-center gap-3 flex">
                    <div className="self-center">
                        <p className="font-bold text-white">Location</p>
                        <input className="bg-grey-50 w-full py-2 font-medium px-3 focus:outline-none focus:shadow-outline"
                            onChange={(e) => setLocation(e.target.value)}
                            value={location}
                        />
                    </div>
                </div>
                <div className="w-1/3 h-4/6 self-center justify-center gap-3 flex flex-col">
                    <div className="flex justify-between">
                    </div>
                    <button onClick={() => activateScraping(job, location)} className="text-2xl font-semibold text-white">Start</button>
                </div>
                <div className="w-1/3 h-4/6 self-center justify-center gap-3 flex flex-col">
                    <div className="flex justify-between">
                    </div>
                    <button onClick={() => setScrapePage(false)} className="text-2xl font-semibold text-amber-200">Close</button>
                </div>
            </div>
            {!scriptExecution &&
                <div onClick={() => play()} className={`mb-8 h-4 bg-green-300 ${play}`}></div>
            }
            {userJobs ?
                <div className="h-svh flex gap-5 ">
                    <div className="pl-20 w-8/12">
                        <h2 className="text-xl font-semibold">History</h2>
                        <p className="text-sm mb-4">( Click play to activate scraping )</p>
                        <div className="flex text-lg font-semibold ">
                            <div className="flex flex-col w-6/12">
                                <p>Job</p>
                                <div className="h-8 flex text-sm font-normal">
                                    <span className="overflow-ellipsis self-center">{cfl(userJobs.job, false)}</span>
                                </div>
                            </div>
                            <div className="flex flex-col w-6/12">
                                <p>Location</p>
                                <div className="h-8 flex text-sm font-normal">
                                    <p className="self-center">{cfl(userJobs.location, true)}</p>
                                </div>
                            </div>
                            <div className="flex flex-col text-center w-1/12">
                                <p>Scrape</p>
                                <button onClick={() => activateScraping(userJobs.job, userJobs.location)}
                                    className="h-8">
                                    <span
                                        className={`text-2xl ${scriptExecution ? 'text-red-500' : 'text-green-500'}`}>
                                        
                                    </span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                : <p>hey</p>}
        </>
    )

}
