# Build Grasshopper .ghuser components in a Linux container -- no Windows, no Rhino.
#
#   docker build -f docker/Dockerfile --target export --output type=local,dest=build .
#
# run from plugin_set/. The .ghuser files land in ./build. The SAME command
# runs on your laptop, in GitHub Actions, and under `act` (Actions run locally),
# because nothing is bind-mounted: the components go IN with COPY, and the
# results come OUT through BuildKit's --output.
#
# Three stages:
#   toolchain  Mono + pythonnet + GH_IO.dll + the COMPAS componentizer, all pinned
#   build      copies components/, packages them, then VERIFIES the result
#   export     only the .ghuser files, so --output gets nothing else
#
# Why Mono: the componentizer is Python, but it writes .ghuser files through
# GH_IO.dll, the .NET library Grasshopper itself uses to save files. On Windows
# that runs on .NET Framework; on Linux, Mono runs the same assembly.

FROM debian:bookworm-slim AS toolchain

# mono-devel, not mono-runtime: pythonnet needs the netstandard facade, which
# Debian ships only in mono-devel. libmonosgen is the runtime pythonnet hosts.
RUN apt-get update && apt-get install -y --no-install-recommends \
        mono-devel libmonosgen-2.0-1 \
        python3 python3-pip curl unzip ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages pythonnet==3.0.3
ENV PYTHONNET_RUNTIME=mono \
    PYTHONNET_MONO_LIBMONO=/usr/lib/libmonosgen-2.0.so.1

# GH_IO.dll from the official Grasshopper NuGet package. Pinned: a .ghuser built
# with a newer GH_IO than the user's Rhino is the classic "component will not
# load" bug, so the version is a decision, not "latest".
ARG GH_VERSION=8.35.26251.13001
RUN mkdir -p /opt/ghio \
    && curl -fsSL "https://www.nuget.org/api/v2/package/Grasshopper/${GH_VERSION}" -o /tmp/gh.nupkg \
    && unzip -j /tmp/gh.nupkg 'lib/net48/GH_IO.dll' -d /opt/ghio \
    && rm /tmp/gh.nupkg

# The COMPAS componentizer (MIT, Gramazio Kohler Research), pinned to the commit
# behind its v5 tag -- the same code the GitHub Action runs.
ARG COMPONENTIZER_SHA=dfec7e4fdb16add832793c1d5715287532841430
RUN curl -fsSL "https://raw.githubusercontent.com/compas-dev/compas-actions.ghpython_components/${COMPONENTIZER_SHA}/componentize_cpy.py" \
        -o /opt/componentize_cpy.py

WORKDIR /work


FROM toolchain AS build
COPY components /work/components
COPY docker/verify_ghuser.py /opt/verify_ghuser.py
# Package, then check what was packaged. If verification fails, the image
# build fails, and nothing is exported -- a broken .ghuser never leaves.
RUN python3 /opt/componentize_cpy.py --ghio /opt/ghio components build \
    && python3 /opt/verify_ghuser.py components build


FROM scratch AS export
COPY --from=build /work/build/ /
