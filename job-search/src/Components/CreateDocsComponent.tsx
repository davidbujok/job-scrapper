import { useState } from "react";
import { Job as JobType } from "../Interfaces"
import OpenAI from 'openai'
import { work, education, traits } from "../assets/cv.tsx"

interface JobComponentProps {
    job: JobType;
}
interface OpenAIResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    choices: [];
}


export default function CreateDocs({ job }: JobComponentProps) {
    const [responseData, setResponseData] = useState<OpenAIResponse | null>(null);
    const openai = new OpenAI({
        apiKey: import.meta.env.VITE_OPENAI_API_KEY,
        dangerouslyAllowBrowser: true
    });
    const prompt_personal_statement = `Write a personal statement that fits recognised cv standards
in UK, limit CV to maximum of 200 words. Consider those things when creating a personal statement:
Work Experiance in order: ${work.self}, ${work.amazon}, ${work.chef}
Education in order: ${education.codeclan}, ${education.rgu}, ${education.fifecollege}, ${education.szybin}
and the person softskills are: ${traits.softskills} and interests: ${traits.interests}
Now you have an imagege of the person that is applying for a job. 
When writing a personal statement use those pieces of information about the person that 
are the best match for this job position ${job.position} and keep in mind this more detailed
description of the job position: ${job.about}. Whenever you can highlight the information about the
person and how they are tightly connected with the requirements in the job description.
`

    async function activateDocsGeneration() {
        try {
            const completion = await openai.chat.completions.create({
                messages: [{
                    role: "user",
                    content: prompt_personal_statement
                }],
                model: "gpt-3.5-turbo",
            });
            return completion; // Returning full completion to handle in the calling method
        } catch (error) {
            console.error("Error while fetching data from OpenAI:", error);
            return null;
        }
    }

    const handleClick = async () => {
        console.log("Generating docs...");
        const completion = await activateDocsGeneration();
        if (completion) {
            setResponseData(completion); // Correctly set response data
        } else {
            //setResponseData("Failed to generate document"); // Error fallback handling
            setResponseData(null); // Error fallback handling
        }
    };
                    //<p key={choice.id}>{choice.message.content}</p>
            //{responseData ?
            //    <p>{responseData.choices[0].message.content}</p> : // Directly render response data
            //    <p>No Document Generated</p> // Fallback content
            //}
    return (
        <>
            <h1>{job.position}</h1>
            <h2>{job.title}</h2>
            <h3>{job.company}</h3>
            <button className="h-10 w-40 bg-red-800 rounded" onClick={handleClick}>
                Generate Docs
            </button>
            {responseData && responseData.choices.length > 0 ?
                responseData.choices.map(choice => (
                    <p>{choice.message.content}</p>
                )) :
                <p>No Document Generated</p>
            }
        </>
    );
}

