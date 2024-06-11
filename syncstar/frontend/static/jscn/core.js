/*
SyncStar
Copyright (C) 2024 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License along
with this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the codebase or documentation
are not subject to the GNU Affero General Public License and may only be used
or replicated with the express permission of Red Hat, Inc.
*/

function demand_disk_sync ( rqstcode ) {
    if (disconnected === false) {
        if (isoshash.trim() !== "" || diskhash.trim() !== "") {
            try {
                let rqstobjc = new XMLHttpRequest();
                rqstobjc.open("GET", `/kick/${rqstcode}/${diskhash}/${isoshash}`, false);
                rqstobjc.send(null);
                if (rqstobjc.status === 403) {
                    invoke_disconnected_window();
                } else {
                    if (rqstobjc.status === 200) {
                        document.getElementById("livenotify-text").innerText = "Task has been successfully scheduled";
                        document.getElementById("livenotify").className = "toast align-items-center text-bg-success border-0";
                    } else {
                        if (rqstobjc.status === 404 && rqstobjc.responseText.includes(diskhash) === true) {
                            document.getElementById("livenotify-text").innerText = "Requested storage device is no longer available";
                        } else if (rqstobjc.status === 404 && rqstobjc.responseText.includes(isoshash) === true) {
                            document.getElementById("livenotify-text").innerText = "Requested images archive is no longer available";
                        } else if (rqstobjc.status === 400) {
                            document.getElementById("livenotify-text").innerText = "Requested storage device cannot be accessed now";
                        } else if (rqstobjc.status === 422) {
                            document.getElementById("livenotify-text").innerText = "Requested image archive exceeds the capacity";
                        }
                        document.getElementById("livenotify").className = "toast align-items-center text-bg-warning border-0";
                    }
                    bootstrap.Toast.getOrCreateInstance(document.getElementById("livenotify")).show();
                    retrieve_time(rqstcode);
                }
            } catch (expt) {
                invoke_disconnected_window();
            }
        } else {
            document.getElementById("livenotify").className = "toast align-items-center text-bg-warning border-0";
            document.getElementById("livenotify-text").innerText = "Storage devices or images archive were not selected";
            bootstrap.Toast.getOrCreateInstance(document.getElementById("livenotify")).show();
        }
    }
}

function invoke_images_select_window ( rqstcode, diskindx ) {
    if (disconnected === false) {
        try {
            let rqstobjc = new XMLHttpRequest();
            rqstobjc.open("GET", `/scan/${rqstcode}/${diskindx}`, false);
            rqstobjc.send(null);

            if (rqstobjc.status === 403) {
                invoke_disconnected_window();
            } else {
                if (rqstobjc.status === 200) {
                    let data = JSON.parse(rqstobjc.responseText);
                    document.getElementById("disk-prim").innerHTML =
                        `${data["disk"]["name"]["vendor"]}&nbsp;${data["disk"]["name"]["handle"]}`;
                    document.getElementById("disk-seco").innerHTML =
                        `<span style="font-weight: bold">${(data["disk"]["size"] / (1024 * 1024 * 1024)).toFixed(2)} GiB</span> on <span style="font-weight: bold;">${data["disk"]["node"]}</span>`;
                    if (Object.keys(data.isos).length === 0) {
                        document.getElementById("isoslist").innerHTML =
                            `
                            <div class="card">
                                <div class="card-body strdelem">
                                    No images detected
                                </div>
                            </div>
                            `;
                    } else {
                        document.getElementById("diskindx").innerHTML = data.indx;
                        document.getElementById("isoslist").innerHTML = "";
                        for (let indx in data.isos) {
                            let elem = data.isos[indx];
                            document.getElementById("isoslist").innerHTML +=
                                `
                                <a class="list-group-item ${(elem['bool'] === true) ? 'border-success' : 'border-warning'} list-group-item-action p-2" id="isos-${indx}" onclick="select_hashes('${indx}', '${diskindx}');">
                                    <div class="d-flex w-100" style="gap: 0.5rem;">
                                        <div style="aspect-ratio: 1/1; height: 50px;">
                                            ${(icondict.hasOwnProperty(elem["type"]) === true) ? `<img src='${iconpath}/${icondict[elem['type']]}' class='w-100 h-100 filter-default' />` : `<img src='${iconpath}/${icondict['common']}' class='w-100 h-100 filter-default' />`}
                                        </div>
                                        <div class="d-flex flex-column flex-grow-1">
                                            <div class="d-flex justify-content-between align-items-start">
                                                <h5 class="mb-1 headelem" id="name-${indx}">${elem["name"]}</h5>
                                                <span class="strdelem badge ${(elem['bool'] === true) ? 'text-bg-success' : 'text-bg-warning'} rounded-pill monotext">
                                                    ${(icondict.hasOwnProperty(elem["type"]) === true) ? `${elem["type"]}` : `common`}
                                                </span>
                                            </div>
                                            <small class="mb-0 secotext text-muted">Requires at least <span class="${(elem['bool'] === true) ? 'text-success' : 'text-warning'}" style="font-weight: bold">${(elem["size"] / (1024 * 1024 * 1024)).toFixed(2)} GiB</span> of storage</small>
                                        </div>
                                    </div>
                                </a>
                                `;
                        }
                    }
                    isoshash = ""; diskhash = "";
                    document.getElementById("isosname").innerHTML = "No images selected";
                    const quesread = new bootstrap.Modal("#quesread");
                    quesread.toggle();
                } else {
                    if (rqstobjc.status === 404) {
                        document.getElementById("livenotify-text").innerText = "Requested storage device is no longer available";
                        retrieve_time(rqstcode);
                    } else if (rqstobjc.status === 400) {
                        document.getElementById("livenotify-text").innerText = "Requested storage device cannot be accessed now";
                    }
                    document.getElementById("livenotify").className = "toast align-items-center text-bg-warning border-0";
                    bootstrap.Toast.getOrCreateInstance(document.getElementById("livenotify")).show();
                }
            }
        } catch(expt) {
            invoke_disconnected_window();
        }
    }
}

function retrieve_time ( rqstcode ) {
    if (disconnected === false) {
        try {
            let rqstobjc = new XMLHttpRequest();
            rqstobjc.open("GET", `/read/${rqstcode}`, false);
            rqstobjc.send(null);

            if (rqstobjc.status === 200) {
                let data = JSON.parse(rqstobjc.responseText);
                document.getElementById("lastupdt").innerText = "Last updated on " + data.time;

                // DEBUG PRINT BELOW
                document.getElementById("debplc").textContent = JSON.stringify(data, undefined, 2);

                if (Object.keys(data.devs).length === 0) {
                    document.getElementById("disklist").innerHTML =
                        `
                        <div class="card">
                            <div class="card-body">
                                No USB storage devices detected
                            </div>
                        </div>
                        `;
                } else {
                    document.getElementById("disklist").innerHTML = "";
                    for (let indx in data.devs) {
                        let disk = data.devs[indx];
                        document.getElementById("disklist").innerHTML +=
                            `
                            <a class="list-group-item list-group-item-action p-2" id="disk-${indx}" onclick="invoke_images_select_window(rqstcode, '${indx}')">
                                <div class="d-flex w-100" style="gap: 0.5rem;">
                                    <div style="aspect-ratio: 1/1; height: 50px;">
                                        <img src="${iconpath}/${icondict['device']}" class="w-100 h-100 filter-default" />
                                    </div>
                                    <div class="d-flex flex-column flex-grow-1">
                                        <div class="d-flex justify-content-between align-items-start">
                                            <h5 class="mb-1 headelem">${disk["name"]["vendor"]}&nbsp;${disk["name"]["handle"]}</h5>
                                            <span class="strdelem badge text-bg-success rounded-pill monotext">${indx}</span>
                                        </div>
                                        <small class="mb-0 secotext text-muted"><span style="font-weight: bold">${(disk["size"] / (1024 * 1024 * 1024)).toFixed(2)} GiB</span> on <span style="font-weight: bold">${disk["node"]}</span></small>
                                    </div>
                                </div>
                            </a>
                            `;
                    }
                }
                if (Object.keys(data.jobs).length === 0) {
                    document.getElementById("proglist").innerHTML =
                        `
                        <div class="card">
                            <div class="card-body strdelem">
                                No running synchronizations detected
                            </div>
                        </div>
                        `;
                } else {
                    document.getElementById("proglist").innerHTML = "";
                    for (let indx in data.jobs) {
                        let prog = data.jobs[indx];
                        document.getElementById("proglist").innerHTML +=
                            `
                            <a class="list-group-item list-group-item-action p-2" id="prog-${indx}">
                                <div class="d-flex w-100" style="gap: 0.5rem;">
                                    <div style="aspect-ratio: 1/1; height: 50px;">
                                        <img 
                                            ${(prog["mood"] === "PENDING") ? "src='" + iconpath + "/" + icondict["lesson"] + "' class='w-100 h-100 filter-pending'" : ""}
                                            ${(prog["mood"] === "FAILURE") ? "src='" + iconpath + "/" + icondict["fiasco"] + "' class='w-100 h-100 filter-failure'" : ""}
                                            ${(prog["mood"] === "WORKING") ? "src='" + iconpath + "/" + icondict["verify"] + "' class='w-100 h-100 filter-working'" : ""}
                                            ${(prog["mood"] === "SUCCESS") ? "src='" + iconpath + "/" + icondict["result"] + "' class='w-100 h-100 filter-success'" : ""}
                                        />
                                    </div>
                                    <div class="d-flex flex-column flex-grow-1">
                                        <div class="d-flex justify-content-between align-items-start">
                                            <h5 class="mb-1 headelem">${prog["disk"]}</h5>
                                            <span 
                                                ${(prog["mood"] === "PENDING") ? "class='strdelem badge rounded-pill monotext text-bg-secondary'" : ""}
                                                ${(prog["mood"] === "WORKING") ? "class='strdelem badge rounded-pill monotext text-bg-warning'" : ""}
                                                ${(prog["mood"] === "FAILURE") ? "class='strdelem badge rounded-pill monotext text-bg-danger'" : ""}
                                                ${(prog["mood"] === "SUCCESS") ? "class='strdelem badge rounded-pill monotext text-bg-success'" : ""}
                                            >
                                                ${indx}
                                            </span>
                                        </div>
                                        <small class="mb-0 secotext text-muted">
                                            ${(prog["mood"] === "PENDING") ? "Waiting for" : ""}
                                            ${(prog["mood"] === "FAILURE") ? "Failed" : ""}
                                            ${(prog["mood"] === "SUCCESS") ? "Completed" : ""}
                                            ${(prog["mood"] === "WORKING") ? "Synchronizing" : "synchronizing"}
                                            <span style="font-weight: bold">${prog["isos"]}</span>
                                            ${(prog["mood"] === "WORKING") ? "since" : "after"}
                                            <span style="font-weight: bold">${prog["time"].toFixed(2)} seconds</span>
                                            (${prog["rcrd"]} records written)
                                        </small>
                                    </div>
                                </div>
                            </a>
                            `;
                    }
                }
            }
            else {
                invoke_disconnected_window();
            }
        } catch(expt) {
            invoke_disconnected_window();
        }
    }
}

function select_hashes ( hashisos, hashdisk ) {
    isoshash = hashisos;
    diskhash = hashdisk;
    document.getElementById("isosname").innerHTML =
        `
        You have selected
        <h5 class="headelem">${document.getElementById("name-" + hashisos).innerText}</h5>
        `;
}

function invoke_disconnected_window () {
    disconnected = true;
    const authrepo = new bootstrap.Modal("#authrepo");
    authrepo.toggle();
}
